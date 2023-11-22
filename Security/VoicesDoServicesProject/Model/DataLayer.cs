using Microsoft.AspNetCore.Http.HttpResults;
using MongoDB.Bson;
using MongoDB.Driver;

public class DataLayer
{
    private readonly IMongoCollection<User> _collection;

    public DataLayer(IMongoClient client)
    {
        var database = client.GetDatabase("Voices-Do-Services-Database");
        _collection = database.GetCollection<User>("Voices-Do-Services-Collection");
    }

    public void InsertMyData(User data)
    {
        _collection.InsertOne(data);
    }
    public async Task UpdateMyDataAsync(string id, User newData)
    {
    newData.Id = ObjectId.Parse(id);
    // Convert string ID to ObjectId
    var objectId = ObjectId.Parse(id);
    var filter = Builders<User>.Filter.Eq(data => data.Id, objectId);
    await _collection.ReplaceOneAsync(filter, newData);
    }
    
    public async Task DeleteMyDataAsync(string id)
    {
        var objectId = ObjectId.Parse(id); // Convert string ID to ObjectId
        var filter = Builders<User>.Filter.Eq(data => data.Id, objectId);
        await _collection.DeleteOneAsync(filter);
    }
    public async Task<User> GetMyDataByEmailAsync(string email)
    {
        return await _collection.Find(data => data.email_login == email).FirstOrDefaultAsync();
    }
    public async Task UpdateMyDataByEmailAsync(string email, User newData)
    {
    // First, find the existing document by email
    var existingData = await _collection.Find(data => data.email_login == email).FirstOrDefaultAsync();
    if (existingData == null)
    {
        return;
    }

    // Update fields of existingData with newData, except for the _id field
    existingData.email_login = existingData.email_login;
    existingData.password_login = newData.password_login;
    existingData.pincode_login = newData.pincode_login;
    existingData.email_service_login_email = newData.email_service_login_email;
    existingData.email_service_login_pass = newData.email_service_login_pass;
    existingData.Netflix_username = newData.Netflix_username;
    existingData.Netflix_pass = newData.Netflix_pass;
    existingData.PrimeVideo_username = newData.PrimeVideo_username;
    existingData.PrimeVideo_pass = newData.PrimeVideo_pass;
    existingData.Spotify_Client_ID = newData.Spotify_Client_ID;
    existingData.Spotify_Client_Secret = newData.Spotify_Client_Secret;
    // Now, replace the existing document with the updated one
    var filter = Builders<User>.Filter.Eq(data => data.email_login, email);
    await _collection.ReplaceOneAsync(filter, existingData);
    }

    public async Task DeleteMyDataByEmailAsync(string email)
    {
        var filter = Builders<User>.Filter.Eq(data => data.email_login, email);
        await _collection.DeleteOneAsync(filter);
    }
}
