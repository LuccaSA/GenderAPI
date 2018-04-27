using GenderAPI.Domain;

namespace GenderAPI.Web.Models
{
    public class Gender
    {
        private string _firstName;
        private string _frenchInsuranceNumber;

        public Gender(IGenderService genderService, string firstName)
            :this(genderService, firstName, string.Empty) { }

        public Gender(IGenderService genderService, string firstName, string frenchInsuranceNumber)
        {
            _firstName = firstName;
            _frenchInsuranceNumber = frenchInsuranceNumber;

            MaleProbability = genderService.MaleProbability(_firstName);
        }

        public decimal MaleProbability { get; private set; }
        public decimal FemaleProbability { get { return 1 - MaleProbability; } }
    }
}
