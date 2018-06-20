using GenderAPI.Controllers;
using GenderAPI.Infra.Services;
using Xunit;

namespace GenderAPI.Tests
{
    public class MachineLearningServiceTests : IClassFixture<DefaultFixture>
    {
        private DefaultFixture _fixture;

        public MachineLearningServiceTests(DefaultFixture fixture)
        {
            _fixture = fixture;
        }

        [Fact]
        public void JeanClaudeShoulbBeAMale()
        {
            using (var scope = _fixture.GetScope())
            {
                var firstName = "Jean";

                var controller = scope.Container.GetInstance<GendersController>();

                var gender = controller.Get(firstName);

                var maleProbability = gender.MaleProbability;

                Assert.True(maleProbability > 0.80M);
            }
        }

        [Fact]
        public void MarieShoulbBeFemale()
        {
            using (var scope = _fixture.GetScope())
            {
                var firstName = "Marie";

                var controller = scope.Container.GetInstance<GendersController>();

                var gender = controller.Get(firstName);

                var femaleProbability = gender.FemaleProbability;

                Assert.True(femaleProbability > 0.80M);
            }
        }
    }
}
