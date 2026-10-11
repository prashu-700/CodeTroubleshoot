# Bug Fix Report — Code Troubleshooting Technical Assessment

## 1. Project Overview

This repository contains two projects submitted for the Code Troubleshooting Technical Assessment:

1. Node.js Book Management Application
2. Python OCR Image Processing Application

The objective was to identify issues, fix bugs, improve application functionality, and verify the changes through testing.

## 2. Node.js Project

### Bug 1: Book Update Operation

**Root Cause:** The book update operation in the controller passed arguments to the service in the incorrect order.

**Fix Applied:** Corrected the argument order so that the update operation receives the expected values.

**File Modified:** `nodejs/src/controllers/bookController.js`

**Testing:** Book management functionality was checked during troubleshooting. Automated tests are available in `nodejs/tests/books.test.js`.

### Bug 2: Local Port Conflict

**Root Cause:** Port 3000 was already occupied by another process, causing an `EADDRINUSE` error when starting the application.

**Resolution:** Identified and stopped the process using the port, then restarted the application successfully.

**Note:** This was a local environment issue rather than a source-code defect.

### Relevant Node.js Files

* `nodejs/src/controllers/bookController.js`
* `nodejs/src/controllers/catalogController.js`
* `nodejs/src/repositories/bookRepository.js`
* `nodejs/src/services/bookService.js`
* `nodejs/src/routes/books.js`
* `nodejs/tests/books.test.js`

## 3. Python OCR Project

### Areas Reviewed and Improved

The Python application processes images and extracts text using Optical Character Recognition (OCR).

The following areas were reviewed during troubleshooting:

* Image preprocessing and readability.
* Image enhancement operations.
* OCR text recognition.
* Image processing pipeline.
* Input validation and error handling.

### Relevant Python Files

* `python/app/preprocessing/image_ops.py`
* `python/app/recognition/ocr.py`
* `python/app/services/pipeline.py`
* `python/app/utils/validation.py`
* `python/app/utils/files.py`
* `python/tests/test_recognize.py`

## 4. Testing Summary

The Node.js and Python projects were tested after the troubleshooting changes.

| Project    | Test File                        | Result |
| ---------- | -------------------------------- | ------ |
| Node.js    | `nodejs/tests/books.test.js`     | PASS   |
| Python OCR | `python/tests/test_recognize.py` | PASS   |

### Testing Performed

* Checked Node.js book management functionality.
* Tested Python OCR recognition functionality.
* Checked application execution during troubleshooting.
* Reviewed the relevant automated test suites.

## 5. Unresolved Issues and Limitations

* OCR accuracy can vary depending on image quality, handwriting, fonts, and noise.
* Additional testing with a wider variety of images and application scenarios is recommended.
* OCR output may require further improvement for difficult or low-quality images.

## 6. Conclusion

The repository contains the Node.js and Python project source code, supporting files, and automated test files. Troubleshooting focused on correcting the Node.js book update argument issue, resolving a local port conflict, and reviewing the Python OCR processing workflow.

The projects are organized in a single public GitHub repository for review and evaluation.
