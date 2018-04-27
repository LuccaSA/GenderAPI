using GenderAPI.Domain;
using GenderAPI.Infra.Config;
using GenderAPI.Infra.Services;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using SimpleInjector;
using SimpleInjector.Lifestyles;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace GenderAPI.Tests
{
    public class DefaultFixture
    {
        private const string _pathToAppSettings = "..//..//..//..//Web//appsettings.json";
        protected Container Container { get; private set; }

        public DefaultFixture()
        {
            Container = new Container();
            Container.Options.DefaultScopedLifestyle = new AsyncScopedLifestyle();

            Container.Register<IOptions<AppSettings>>(() =>
                Options.Create(JsonConvert.DeserializeObject<AppSettings>(File.ReadAllText(_pathToAppSettings)))
            , Lifestyle.Scoped);
            Container.Register<IGenderService, MachineLearningService>(Lifestyle.Scoped);
        }

        public Scope GetScope()
        {
            return AsyncScopedLifestyle.BeginScope(Container);
        }

        public T GetInstance<T>()
            where T : class
        {
            return Container.GetInstance<T>();
        }
    }
}
