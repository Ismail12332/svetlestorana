<script>
    import Auth0 from 'auth0-js';
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-navigator'
  
    const webAuth = new Auth0.WebAuth({
        domain: 'dev-whbba5qnfveb88fc.us.auth0.com',
        clientID: 'lmZzOfWN5OU25eodYKHpgPaiN67UQ5m3',
        redirectUri: 'https://survzilla.onrender.com/glav',
        responseType: 'token id_token',
        scope: 'openid profile email offline_access',
        audience: 'http://Survzilla'
    });
  
    const login = () => {
        webAuth.authorize();
    };


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
      }
      });
  });

  </script>
  
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
  </style>
  
  <div class="login-container">
    <div class="login-box">
      <div class="login-title">Survzilla</div>
      <button class="login-button" on:click={login}>Continue</button>
    </div>
  </div>
  