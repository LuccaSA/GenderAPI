using GenderAPI.Domain;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace GenderAPI.Infra
{
    public class MachineLearningService : IGenderService
    {
        private string _filePath;
        private const string _python = "C:\\Users\\Nfaugout\\AppData\\Local\\Programs\\Python\\Python36\\python.exe";

        public MachineLearningService(string filePath)
        {
            _filePath = filePath;
        }

        public decimal MaleProbability(string firstName)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = _python;
            start.Arguments = string.Format("{0} {1}", _filePath, firstName);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    var result = JsonConvert.DeserializeObject<decimal[]>(reader.ReadToEnd().Replace(" ]", "]").Replace(" ", ","));

                    return result[0];
                }
            }
        }
    }
}
