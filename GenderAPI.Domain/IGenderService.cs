using System.Collections.Generic;

namespace GenderAPI.Domain
{
    public interface IGenderService
    {
        decimal MaleProbability(string firstName);
    }
}
