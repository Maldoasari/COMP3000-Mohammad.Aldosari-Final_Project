using Microsoft.AspNetCore.Mvc;

[Route("api/Voices-Do-services")]
[ApiController]
public class MyController : ControllerBase
{
    private readonly DataLayer _dataLayer;

    public MyController(DataLayer dataLayer)
    {
        _dataLayer = dataLayer;
    }

    [HttpGet("ByEmail/{email}")]
    public async Task<IActionResult> GetDataByEmail(string email)
    {
        var data = await _dataLayer.GetMyDataByEmailAsync(email);
        if (data == null)
        {
            return NotFound();
        }

        return Ok(data);
    }
    [HttpPost]
    public IActionResult CreateData(MyDataModel model)
    {
        _dataLayer.InsertMyData(model);
        return Ok();
    }
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateData(string id, [FromBody] MyDataModel newData)
    {
        await _dataLayer.UpdateMyDataAsync(id, newData);
        return Ok();
    }
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteData(string id)
    {
        await _dataLayer.DeleteMyDataAsync(id);
        return Ok();
    }

    [HttpPut("ByEmail/{email}")]
    public async Task<IActionResult> UpdateDataByEmail(string email, [FromBody] MyDataModel newData)
    {
        var data = await _dataLayer.GetMyDataByEmailAsync(email);
        if (data == null)
        {
            return NotFound();
        }
        await _dataLayer.UpdateMyDataByEmailAsync(email, newData);
        return Ok();
    }

    [HttpDelete("ByEmail/{email}")]
    public async Task<IActionResult> DeleteDataByEmail(string email)
    {
        var data = await _dataLayer.GetMyDataByEmailAsync(email);
        if (data == null)
        {
            return NotFound();
        }
        await _dataLayer.DeleteMyDataByEmailAsync(email);
        return Ok();
    }

}