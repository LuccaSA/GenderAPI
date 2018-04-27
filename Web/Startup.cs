using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using GenderAPI.Domain;
using GenderAPI.Infra;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace GenderAPI
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc();

            //var csvFilePath = "C:\\Lucca\\2018 - SWE Nantes\\GenderAPI\\Data\\unique_genders.csv";
            var pythonFilePath = "C:\\Lucca\\2018 - SWE Nantes\\GenderMachine\\genderService.py";

            services.AddScoped<IGenderService>((provider) => new MachineLearningService(pythonFilePath));
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseMvc();
        }
    }
}
