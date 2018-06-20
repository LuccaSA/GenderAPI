namespace GenderAPI.Infra.Config
{
    public class AppSettings
    {
        public Python Python { get; set; }
        public Csv Csv { get; set; }
    }

    public class Python
    {
        public string PathToPython { get; set; }
        public string PathToGenderService { get; set; }
    }

    public class Csv
    {
        public string PathToVocabulary { get; set; }
    }
}
