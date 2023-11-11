using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[Route("api/Voices-Do-services")]
[ApiController]
//[Authorize(AuthenticationSchemes = "ApiKeyAuth")]
public class MyController : ControllerBase
{
    [Route("/[action]")]
    [HttpGet]
    public IActionResult Get()
    {
        return Ok("Access Granted. You have successfully called the API.");
    }

    // Add other actions here
}
