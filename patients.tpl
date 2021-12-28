<!doctype html>
<html>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Hospital Database - {{ title }}</title>
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
    <h2>{{head}}</h2>
    <h4>You may remove a patient for the doctor here or use the button below to add a new patient</h4>
    <a class="btn btn-primary" href="/patients/{{id}}/add">Add Patient <span class="sr-only"></span></a>
    <table class='table table-striped'>
    % for header in headers:
        <th>{{header}}</th>
    % end
    <th>Remove Patient</th>
    % for row in table:
        <tr>
        % for cell in row:
            <td>{{str(cell)}}</td>
        % end
        <td><a href="/patients/{{id}}/remove/{{str(row[0])}}">Remove</a></td>
        </tr>
    % end
    </table>
    </div>
    <div id="footer">
    </div>
  </body>
</html>