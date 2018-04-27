using GenderAPI.Controllers;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using Newtonsoft.Json;
using System;
using System.Diagnostics;
using System.IO;
using Xunit;

namespace GenderAPI.Tests
{
    public class UnitTest1
    {
        [Fact]
        public void JeanClaudeShoulbBeAMale()
        {
            var firstName = "Jean Claude";

            var api = new GendersController(null);

            var gender = api.Get(firstName);

            var maleProbability = gender.MaleProbability;

            Assert.True(maleProbability > 0.9M);
        }

        [Fact]
        public void MarieShoulbBeFemale()
        {
            var firstName = "Marie";

            var api = new GendersController(null);

            var gender = api.Get(firstName);

            var femaleProbability = gender.FemaleProbability;

            Assert.True(femaleProbability > 0.9M);
        }

        [Fact]
        public void Toto()
        {
            var python = "C:\\Users\\Nfaugout\\AppData\\Local\\Programs\\Python\\Python36\\python.exe";
            var file = "C:\\Lucca\\genderService.py";
            var cmd = "C:\\Windows\\System32\\cmd.exe";

            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = python;
            start.Arguments = string.Format("{0} {1}", file, "Marie");//, "C:\\Lucca\\2018 - SWE Nantes\\GenderMachine\\hello.py");
            start.UseShellExecute = false;
            start.CreateNoWindow = true;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string stderr = process.StandardError.ReadToEnd(); // Here are the exceptions from our Python script
                    string result = reader.ReadToEnd(); // Here is the result of StdOut(for example: print "test")

                    Assert.NotEmpty(result);
                }
            }

            //Process p = new Process();
            //p.StartInfo = new ProcessStartInfo(python, file)
            //{
            //    RedirectStandardOutput = true,
            //    UseShellExecute = false,
            //    CreateNoWindow = true
            //};
            //p.Start();

            //string output = p.StandardOutput.ReadToEnd();
            //p.WaitForExit();

            //Assert.Equal("Hello", output);
            //ScriptEngine engine = Python.CreateEngine();
            //dynamic scope = engine.CreateScope();
            //engine.ExecuteFile(file);
            //var x = scope.get_x();
        }
    }
}
