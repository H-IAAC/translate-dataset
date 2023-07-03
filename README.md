# Translate Dataset

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This project provides tools for translating datasets using the Google Translate API.

## Team

* Coordinator: Sildolfo Gomes (sildolfo.neto@eldorado.org.br)

## Introduction

The Translate Dataset project aims to provide a convenient way to translate datasets using the Google Translate API. It is designed to handle CSV files, break down the text in each field, translate it, and then merge it back into a new CSV file.

## How to Use

To utilize the current translation module, follow these steps:

1. Create an account on the Google Cloud Platform (GCP).
2. Generate a Google Translate API key by enabling the Google Translate service.
3. Generate a JSON file containing the necessary credentials.
4. Place the JSON file in the root folder of the system (a more secure method will be implemented later).
5. Access the JSON file within the translation script.

Once you have set up the necessary credentials, you can proceed with the following steps:

1. Verify any restrictions in the CSV file.
2. Break down the texts in the CSV file.
3. Translate the texts.
4. Merge the translated texts back into a new CSV file.

## Requirements

To use this module, you need to have the following:

* Python 3.6 or higher
* Google Translate API key
* CSV file to translate

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sildolfo/translate-dataset.git
