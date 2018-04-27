using GenderAPI.Domain;
using GenderAPI.Domain.Models;
using Microsoft.AspNetCore.Mvc;

namespace GenderAPI.Controllers
{
    [Route("api/[controller]")]
    public class GendersController : Controller
    {
        private IGenderService _genderService;

        public GendersController(IGenderService genderService)
        {
            _genderService = genderService;
        }

        // GET api/gender
        [HttpGet]
        public Gender Get(string firstName)
        {
            return new Gender(_genderService, firstName);
        }
    }
}
