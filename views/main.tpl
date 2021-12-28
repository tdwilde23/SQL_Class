<!doctype html>
<html>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Hospital Database</title>
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
    <h4>Use the form below to search for a doctor by first name or specialty</h4>
    <form action="/search" method="POST">
        First Name: <input class="form-control form-control-lg" name="firstname" type="text"/><br>
        <label for="specialty">Specialty:</label>
        <select class="form-control form-control-lg" name="specialty" id="specialty">
            % for specialty in specialties:
                <option value="{{specialty}}">{{specialty}}</option>
            % end
        </select><br>
        <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    <div id="footer">
    </div>
  </body>
</html>
