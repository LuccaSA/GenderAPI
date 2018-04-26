using System.Collections.Generic;

namespace GenderAPI.Domain
{
    public interface IFirstNamesDictionary
    {
        Dictionary<string, string> FirstNamesToGender { get; }
    }
}
