using GenderAPI.Domain;
using GenderAPI.Infra.Config;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using System.Diagnostics;
using System.IO;

namespace GenderAPI.Infra.Services
{
    public class MachineLearningService : IGenderService
    {
        private IOptions<AppSettings> _appSettings;

        public MachineLearningService(IOptions<AppSettings> appSettings)
        {
            _appSettings = appSettings;
        }

        public decimal MaleProbability(string firstName)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = _appSettings.Value.Python.PathToPython;
            start.Arguments = string.Format("{0} {1}", _appSettings.Value.Python.PathToGenderService, firstName);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    //Output is like "[0.95 0.05 ]"
                    //or like "[0.95  0.05]\r\n"
                    var output = reader.ReadToEnd();
                    output = output.Replace(" ]", "]").Replace("  ", ",").Replace(" ", ",").Replace("\r\n", "");

                    var result = JsonConvert.DeserializeObject<decimal[]>(output);

                    return result[0];
                }
            }
        }
    }
}
