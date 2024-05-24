<script>
    export let webAuth;
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import Auth0 from 'auth0-js';



    const login = () => {
        webAuth.authorize();
    };


    let vitrineProjects = writable([]);

    onMount(async () => {
        const response = await fetch('http://127.0.0.1:5000/api/vitrine', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
        });

        if (response.ok) {
        const data = await response.json();
        vitrineProjects.set(data.projects);
        } else {
        console.error('Failed to fetch vitrine projects.');
        }
    });
</script>

<style>
    .container {
        text-align: center;
        margin-top: 50px;
    }
    .projects {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 20px;
    }
    .project-card {
        border: 1px solid #ccc;
        border-radius: 10px;
        margin: 10px;
        padding: 20px;
        width: 200px;
        text-align: center;
    }
    .project-card img {
        max-width: 100%;
        height: auto;
        border-radius: 5px;
    }
</style>

<div class="container">
    <h1>Welcome to Survzilla</h1>
    <button on:click={login}>Login</button>
    <h2>Projects Showcase</h2>
    <div class="projects">
        {#each $vitrineProjects as project}
        <div class="project-card">
            <h3>{project.vessel_name}</h3>
            <img src={project.gen_info_image} alt="Vessel Image">
            <p>Price: ${project.price}</p>
        </div>
        {/each}
    </div>
</div>
