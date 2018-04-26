using GenderAPI.Controllers;
using System;
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
    }
}
