import * as fs from "fs";
// import * as https from "https";
import * as path from "path";
import { promisify } from "util";

const readdir = promisify(fs.readdir);
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);


// Output status message with success/failure indicator
function infoStatus(msgBody: string, status: number): void {
    const msgSuccess = "\u2705";  // Unicode for white heavy check mark
    const msgFailed = "\u274C";   // Unicode for cross mark
    const msgWarn = "\u2139";
    if (status === 0) {
        console.log(`${msgSuccess} ${msgBody}`);
    }
    else if (status === 1) {
        console.log(`${msgFailed} ${msgBody}`);
    }
    else {
        console.log(`${msgWarn} ${msgBody}`);
    }
}

function processGetStatus(defaultStatus: number = 0){
    // In TypeScript, we need to pass the status explicitly since we don't have $?
    return process.exitCode || defaultStatus;
}
function processExit(exitCode: number = 1){
    process.exit(exitCode);
}
function processGetArgv(sliceStart:number=2){
    return process.argv.slice(sliceStart);
}
// define a option to accept custom functions
// type CustomHooks = Record<string, (...args:any) => Promise<unknown>>;
// function nothing(...args:any) {
// }
// const defaultProcessHooks :CustomHooks= {
//     processGetStatus: async (defaultStatus: number = 0) => {
//        return defaultStatus
//     },
//     processExit: async (exitCode: number = 1) => {
//     }
// };

// const processHooks :CustomHooks= {
//     processGetStatus: async (defaultStatus: number = 0) => {
//        return processGetStatus(defaultStatus);
//     },
//     processExit: async (exitCode: number = 1) => {
//         processExit(exitCode)
//     },
// };
// /**
//  * get custom hook safely with fallback to nothing
//  */
// function getHook(name:string,hooks:CustomHooks={}){
//     let func = hooks[name] || defaultProcessHooks[name] || nothing;
//     return func;
// }


// Check result and output success/failure message
function checkResult(msgBody: string, flagExit: boolean = false): void {
    const msgSuccess = "\u2705";  // Unicode for white heavy check mark
    const msgFailed = "\u274C";   // Unicode for cross mark

    // In TypeScript, we need to pass the status explicitly since we don't have $?
    const status = processGetStatus(0);
    if (status === 0) {
        infoStatus(msgBody,0)
    } else {
        infoStatus(msgBody,1)
        if (flagExit) {
            processExit(1)
        }
    }
}

// Add padding to message with dashes
function msgPadd(msg: string, msgMaxLen: number): string {
    const msgLen = msg.length;
    const msgFillLength = Math.floor((msgMaxLen - msgLen + 2) / 2);
    const msgPadding = "-".repeat(msgFillLength);

    return `${msgPadding}-${msg}-${msgPadding}`.substring(0, msgMaxLen);
}

// Format step information with padding
function infoStep(msg: string): void {
    console.log(msgPadd(msg, 60));
}




/**
 * convert string or string array to normalized array
 * @example
 * ```ts
 * tostra(".json,.txt") // [".json", ".txt"]
 * ```
 */
function tostra(v: string | string[]) {
    return typeof v === "string"
        ? v
                .split(",")                  // Split by comma
                .map((v) => v.trim().toLowerCase())  // Trim whitespace and convert to lowercase
                .filter((v) => v)         // Remove empty strings
        : v;
}

// Read all text files in the specified directory
async function readTextFilesInDirectory(dirPath: string): Promise<string[]> {
    // Define allowed file extensions (.json and .txt)
    let exts = tostra(`.json,.txt`);

    // Read all files in the directory
    const files = await readdir(dirPath);
    const textFiles: string[] = [];

    // Iterate through each file in the directory
    for (const file of files) {
        // Get the full path of the file
        const filePath = path.join(dirPath, file);
        // Get file statistics
        const stat = await promisify(fs.stat)(filePath);

        // Get file extension in lowercase
        let extname = path.extname(file).toLowerCase();

        // If it's a file and has an allowed extension, add it to the result array
        if (stat.isFile() && exts.some((v) => v === extname)) {
            textFiles.push(filePath);
        }
    }
    return textFiles;
}

type Found = { fileName: string; foundText: string[] };

// Search for text or regex pattern in multiple files
async function findTextInFiles(
    // Array of file paths to search in
    files: string[],
    // Search pattern: can be either a string or regular expression
    searchText: string | RegExp
): Promise<Found[]> {
    // Array to store search results
    const results: Found[] = [];

    // Process each file
    for (const file of files) {
        // Read file content with UTF-8 encoding
        const content = await readFile(file, "utf-8");
        // Array to store matched text for current file
        const matches: string[] = [];

        // Handle string search
        if (typeof searchText === "string") {
            // Find all occurrences of the search text
            let index = content.indexOf(searchText);
            while (index !== -1) {
                matches.push(searchText);
                // Continue searching from the end of last match
                index = content.indexOf(searchText, index + searchText.length);
            }
        }
        // Handle regex search
        else {
            // Find all matches using regular expression
            const regexMatches = content.match(searchText);
            if (regexMatches) {
                matches.push(...regexMatches);
            }
        }

        // If matches found, add to results
        if (matches.length > 0) {
            results.push({ fileName: file, foundText: matches });
        }
    }
    return results;
}

// text replace in files
async function replaceTextInFiles(
    results: { fileName: string; foundText: string[] }[],
    searchText: string | RegExp,
    replaceText: string
): Promise<void> {
    for (const result of results) {
        const content = await readFile(result.fileName, "utf-8");
        const newContent = content.replace(searchText, replaceText);
        await writeFile(result.fileName, newContent, "utf-8");
    }
}

// todo:
// text --code--> type + flag --parse--> nano


const { log } = console;
async function main() {
    let stepName="";

    stepName="get args from command line";
    infoStep(stepName);
    let argv = processGetArgv(2)
    // args to oneline string
    let stro = JSON.stringify(argv, null, 0);
    log(`[args] ${stro}`);
    infoStatus(stepName,0);


    let [dir, pattern, replace] = argv;
    // let reg = new RegExp(pattern, "ig");
    // // log(reg);
    const directoryPath = dir
        ? dir
        : "D:/code/powershell/scoop_bucket_cn/bucket"; // 替换为实际的目录路径
    // const searchText = pattern ? reg : /hello/g; // 可以是字符串或正则表达式
    // const replaceText = replace !== undefined ? replace : "world";

    stepName="read search text and replace text";
    infoStep(stepName);
    let searchText = await readFile(pattern, "utf-8");
    let replaceText = await readFile(replace, "utf-8");
    searchText=searchText.trim();
    replaceText=replaceText.trim();

    log(`[searchText] ${searchText}\n[replaceText] ${replaceText}`);

    infoStatus(stepName,0);

    if (searchText == replaceText) return;

    try {
        stepName="read file path of bucket files";
        infoStep(stepName);
        const textFiles = await readTextFilesInDirectory(directoryPath);
        log(`[bucket]\n${textFiles.join("\n")}`);
        infoStatus(stepName,0);

        stepName="read search text in bucket files";
        infoStep(stepName);
        const searchResults = await findTextInFiles(textFiles, searchText);
        let foundx = searchResults
            .map((v) => {
                let { foundText } = v;
                return foundText.map((v) => v.trim()).join("\n");
            })
            .join("\n");
            foundx=foundx.trim();
        log(`[found]\n${foundx}`);
        infoStatus(stepName,0);

        if (replace !== undefined) {
            stepName="replace search text in bucket files";
            infoStep(stepName);
            await replaceTextInFiles(searchResults, searchText, replaceText);
            infoStatus(stepName,0);
        }

        stepName="update ghproxy-url.txt file";
        await writeFile(pattern, replaceText);
        infoStatus(stepName,0);
    } catch (error) {
        infoStatus(stepName,1);
        // console.error(error);
    }
}

main();
