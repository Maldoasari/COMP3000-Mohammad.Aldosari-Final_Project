using System.Threading.Tasks;

public interface IDataLayer
{
    Task InsertMyDataAsync(MyDataModel data);
    // Add other method signatures as needed
}
