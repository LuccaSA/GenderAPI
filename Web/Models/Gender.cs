using GenderAPI.Domain;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GenderAPI.Web.Models
{
    public class Gender
    {
        private string _firstName;
        private string _frenchInsuranceNumber;

        public Gender(IFirstNamesDictionary firstNamesToGenderDictionary, string firstName)
            :this(firstNamesToGenderDictionary, firstName, string.Empty) { }

        public Gender(IFirstNamesDictionary firstNamesToGenderDictionary, string firstName, string frenchInsuranceNumber)
        {
            _firstName = firstName;
            _frenchInsuranceNumber = frenchInsuranceNumber;

            var dico = firstNamesToGenderDictionary.FirstNamesToGender;

            if (dico.ContainsKey(firstName))
            {
                var mrOrMs = dico[firstName];

                if (mrOrMs == "Mr")
                {
                    MaleProbability = 1;
                }
                else
                {
                    MaleProbability = 0;
                }
            }
            else
            {
                MaleProbability = 0.5M;
            }
        }

        public decimal MaleProbability { get; private set; }
        public decimal FemaleProbability { get { return 1 - MaleProbability; } }
    }
}
