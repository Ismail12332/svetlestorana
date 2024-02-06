<script>
  import { Router, Route, Link } from 'svelte-navigator'
  import { navigate } from 'svelte-navigator'
  import { onMount } from 'svelte';
  import Glav from './Glav.svelte'
  import NotFoundPage from './NotFoundPage.svelte'
  import EditProject from "./EditProject.svelte"
  import Auth0 from 'auth0-js';

  const webAuth = new Auth0.WebAuth({
      domain: 'dev-whbba5qnfveb88fc.us.auth0.com',
      clientID: 'lmZzOfWN5OU25eodYKHpgPaiN67UQ5m3',
      redirectUri: 'https://survzilla-frontend-finish.onrender.com/',
      responseType: 'token id_token',
      scope: 'openid profile email',
  });

  const login = () => {
      webAuth.authorize();
  };

  onMount(() => {
      // Check for the authentication result
      webAuth.parseHash((err, authResult) => {
      if (authResult && authResult.accessToken && authResult.idToken) {
          // Handle successful authentication, e.g., store tokens
          console.log('Authentication successful:', authResult);
          const userId = authResult.idTokenPayload.sub; // assuming 'sub' is the user_id
          localStorage.setItem('user_id', userId);
          navigate('/glav')
      } else if (err) {
          // Handle authentication error
          console.error('Authentication error:', err);
      }
      });
  });
</script>



<Router>
  <Route path='/'>
    <div class="for_login">
      <button class="Login" on:click={login}>Login with Google</button>
    </div>
  </Route>

  <Route path='/glav'>
    <Glav />
  </Route>

  <Route path='/EditProject/:project_id'>
    <EditProject/>
  </Route>

  <Route path="/*">
    <NotFoundPage />
  </Route>
</Router>

<style>
  .Login {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
    font-family: inherit;
    background-color: #524646;
    cursor: pointer;
    transition: border-color 0.25s;
    place-items: center;
    display: flex;
  }

  .for_login {
    margin: 0;
    display: flex;
    place-items: center;
    min-width: 320px;
    min-height: 100vh;
    justify-content: center;
  }
</style>