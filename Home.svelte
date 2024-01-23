<script>
    import { onMount } from 'svelte';
    import Auth0 from 'auth0-js';

    const webAuth = new Auth0.WebAuth({
        domain: 'dev-whbba5qnfveb88fc.us.auth0.com',
        clientID: 'lmZzOfWN5OU25eodYKHpgPaiN67UQ5m3',
        redirectUri: 'http://localhost:5173/callback',
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
        } else if (err) {
            // Handle authentication error
            console.error('Authentication error:', err);
        }
        });
    });
</script>

<button on:click={login}>Login with Google</button>