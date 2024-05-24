<script>
  import { Router, Route, Link } from 'svelte-navigator'
  import { navigate } from 'svelte-navigator'
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import HomePage from './HomePage.svelte';
  import LoginPage from './LoginPage.svelte';
  import ViewPdf from './ViewPdf.svelte';
  import Glav from './Glav.svelte'
  import NotFoundPage from './NotFoundPage.svelte'
  import EditProject from "./EditProject.svelte"
  import Auth0 from 'auth0-js';

  const webAuth = new Auth0.WebAuth({
      domain: 'dev-whbba5qnfveb88fc.us.auth0.com',
      clientID: 'lmZzOfWN5OU25eodYKHpgPaiN67UQ5m3',
      redirectUri: 'http://localhost:5173/glav',
      responseType: 'token id_token',
      scope: 'openid profile email',
      audience: 'http://Survzilla'
  });

  onMount(() => {
      // Check for the authentication result
      webAuth.parseHash((err, authResult) => {
      if (authResult && authResult.accessToken && authResult.idToken) {
          // localStorage.setItem('idToken', authResult.idToken);
          localStorage.setItem('accessToken', authResult.accessToken);
          // Handle successful authentication, e.g., store tokens
          console.log('Authentication successful:', authResult);
          const userId = authResult.idTokenPayload.sub; // assuming 'sub' is the user_id
          localStorage.setItem('user_id', userId);
          localStorage.setItem('user_name', authResult.idTokenPayload.name);
          localStorage.setItem('user_avatar', authResult.idTokenPayload.picture);

          navigate('/glav')
      } else if (err) {
          // Handle authentication error
          console.error('Authentication error:', err);
          navigate('/')
      }
      });
  });
</script>



<Router>
  <Route path='/'>
    <HomePage {webAuth}/>
  </Route>

  <Route path='/glav'>
    <Glav {webAuth} />
  </Route>

  <Route path='/EditProject/:project_id'>
    <EditProject {webAuth} />
  </Route>

  <Route path='/view_project_report/:filename'>
    <ViewPdf />
  </Route>

  <Route path="/*">
    <NotFoundPage />
  </Route>
</Router>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
  
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #1e1e1e 0%, #323232 100%);
    font-family: 'Roboto', sans-serif;
  }
  .login-box {
    background: #2e2e2e;
    padding: 3rem 5rem;
    border-radius: 20px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    text-align: center;
    color: #ffffff;
  }
  .login-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    font-weight: 700;
    color: #e0e0e0;
  }
  .login-button {
    display: inline-block;
    padding: 0.75rem 3rem;
    font-size: 1.2rem;
    color: white;
    background: #007bff;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
    text-transform: uppercase;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.4);
  }
  .login-button:hover {
    background: #0056b3;
    transform: translateY(-2px);
  }
  .login-button:active {
    transform: translateY(0);
  }

  :global(body) {
    margin: 0;
    font-family: 'Open Sans', sans-serif; /* Замените 'Open Sans' на любой шрифт, который вы хотите использовать */
    font-size: 16px;
  }
  
</style>