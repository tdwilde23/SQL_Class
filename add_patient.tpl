<!doctype html>
<html>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Hospital Database - {{title}}</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="/">Homepage</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="/listall">All Doctors <span class="sr-only"></span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/insert">Add A Doctor </a>
          </li>
        </ul>
      </div>
    </nav>
    <div id="content">
    <h3>Use the form below to input new patient information</h3>
    <h4>All fields must be filled</h4>
    <form action="/patients/{{id}}" method="POST">
        First Name: <input name="firstname" type="text" required /><br>
        Last Name: <input name="lastname" type="text" required/><br>
        Room Number: <input name="r_number" type="number" max="200" min="100"/><br>
        <input value="Add" type="submit" />
        </form>
    <h4>Or you may select an existing patient to switch to this doctor</h4>
    <table class='table table-striped'>
    % for header in headers:
        <th>{{header}}</th>
    % end
    <th>Add Patient</th>
    % for row in table:
        <tr>
        % for cell in row:
            <td>{{str(cell)}}</td>
        % end
        <td><a href="/patients/{{id}}/switch/{{str(row[0])}}">Add</a></td>
        </tr>
    % end
    </table>
    </div>
    <div id="footer">
    </div>
  </body>
</html>