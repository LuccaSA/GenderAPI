﻿using GenderAPI.Domain;
using GenderAPI.Infra.Config;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace GenderAPI.Infra.Services
{
    public class CsvDictionaryService : IGenderService
    {
        private const char CSVDelimiter = ';';
        private IOptions<AppSettings> _appSettings;

        public CsvDictionaryService(IOptions<AppSettings> appSettings)
        {
            _appSettings = appSettings;
        }

        public decimal MaleProbability(string firstName)
        {
            var dico = ReadCSVFile(_appSettings.Value.Csv.PathToVocabulary, CSVDelimiter);

            if (dico.ContainsKey(firstName))
            {
                var mrOrMs = dico[firstName];

                if (mrOrMs == "Mr")
                {
                    return 1;
                }
                else
                {
                    return 0;
                }
            }
            else
            {
                return 0.5M;
            }
        }

        private Dictionary<string, string> ReadCSVFile(string filename, char csvDelimiter)
        {
            var result = new Dictionary<string, string>();
            var namesCivilTitlesDictionary = new Dictionary<string, string>();

            string line;
            int currentLineNumber = 0;
            int columnCount = 0;

            // Read the file and display it line by line.  
            using (StreamReader file = new StreamReader(filename))
            {
                while ((line = file.ReadLine()) != null)
                {
                    currentLineNumber++;
                    string[] lineString = line.Split(csvDelimiter);
                    // save column count of first line
                    if (currentLineNumber == 1)
                    {
                        columnCount = lineString.Count();
                    }
                    else
                    {
                        //Check column count of every other lines
                        if (lineString.Count() != 3)
                        {
                            throw new Exception(string.Format("CSV Import Exception: Wrong column count in line {0}. Every line must contain two columns.", currentLineNumber));
                        }
                    }

                    if (currentLineNumber > 1)
                    {
                        if (!namesCivilTitlesDictionary.ContainsKey(lineString[0]))
                        {
                            var mrOrMs = lineString[1] == "1" ? "Mr" : "Ms";

                            namesCivilTitlesDictionary.Add(lineString[0], mrOrMs);
                        }
                    }
                }

            }

            return namesCivilTitlesDictionary;
        }
    }
}
