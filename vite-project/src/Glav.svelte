<script>
    import { writable } from 'svelte/store';
    import { createEventDispatcher } from "svelte";
    import { onMount,afterUpdate } from 'svelte';
    import { readable } from 'svelte/store';
    import { Link } from "svelte-navigator";

    const dispatch = createEventDispatcher();

    const first_name = writable('');
    const last_name = writable('');
    const city = writable('');
    const phone = writable('');
    const post = writable('');
    const vessel_name = writable('');
    
    let projects = writable([]);

    onMount(() => {
        fetchProjects();
    });

    afterUpdate(() => {
        // После обновления компонента выполните повторный запрос к серверу
        fetchProjects();
    });


    const createProject = async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const user_id = localStorage.getItem('user_id'); // Get user_id from localStorage

        const response = await fetch('http://127.0.0.1:5000/index2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user_id}`
            },
            body: JSON.stringify({
                user_id: user_id, // Include user_id in the request body
                first_name: $first_name,
                last_name: $last_name,
                city: $city,
                phone: $phone,
                post: $post,
                vessel_name: $vessel_name
            }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Update the projects store with the newly created project
                projects.update(existingProjects => [...existingProjects, {
                    _id: data.project_id,
                    first_name: $first_name,
                    last_name: $last_name,
                    city: $city,
                    phone: $phone,
                    post: $post,
                    vessel_name: $vessel_name,
                    created_at: new Date().toISOString(),  // Update with the current date/time
                    user_id: user_id,
                }]);
                // Notify the parent component about the successful project creation
                dispatch('projectCreated', { project_id: data.project_id });
            } else {
                console.error('Failed to create project.');
            }
        } else {
            console.error('Failed to create project.');
        }
    };
    
    //const logout = () => {
    //    localStorage.removeItem('user_id');
    //    isLoggedIn = false;
    //};


    const fetchProjects = async () => {
        const user_id = localStorage.getItem('user_id');

        // Send a GET request to fetch projects
        const response = await fetch(`http://127.0.0.1:5000/glav?user_id=${user_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user_id}`
            },
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Set the projects store with the fetched projects
                projects.set(data.projects);
            } else {
                console.error('Failed to fetch projects.');
            }
        } else {
            console.error('Failed to fetch projects.');
        }
    };

    // Fetch projects when the component is mounted
    //onMount(fetchProjects);
    
</script>

<style>

@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css');
    

form {
    width: 100%;

}

main {
    width: 100%;
    height: 1200px;
    background: linear-gradient(to bottom, #011a2b, #011529);
}

h1,h2 {
    color: #fff;
}

label {
    color: #fff;
}

p,ul {
    color: #fff;
}



.project-info {
    display: flex;
    margin: 3%;
    flex: 1; /* Равное распределение доступного пространства между дочерними элементами */
    border: 1px solid #000; /* Добавьте границу, чтобы лучше видеть разделение */
    padding: 10px;
    background-color: #191d32;
    justify-content: space-around;
}
    
</style>

<!-- <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
</head> -->


    <main>
        <h1>Survzilla</h1>
        <Link to='/' class="btn btn-danger">Выйти</Link>
        
        <form class="row g-3 needs-validation"  method="POST"  novalidate on:submit={createProject}>
                <div class="col-md-4">
                    <label for="validationCustom01" class="form-label">First name</label>
                    <input type="text" class="form-control" id="validationCustom01"  name="first_name" bind:value={$first_name} required>
                    <div class="valid-feedback">
                    Looks good!
                </div>
                </div>
                <div class="col-md-4">
                    <label for="validationCustom02" class="form-label">Last name</label>
                    <input type="text" class="form-control" id="validationCustom02" name="last_name" bind:value={$last_name} required>
                    <div class="valid-feedback">
                    Looks good!
                </div>
                </div>
                <div class="col-md-4">
                    <label for="validationCustomUsername" class="form-label">post</label>
                    <div class="input-group has-validation">
                    <span class="input-group-text" id="inputGroupPrepend">@</span>
                    <input type="text" class="form-control" id="validationCustomUsername" name="post" bind:value={$post} aria-describedby="inputGroupPrepend" required>
                    <div class="invalid-feedback">
                        Please choose a username.
                    </div>
                </div>
                </div>
                <div class="col-md-6">
                    <label for="validationCustom03" class="form-label">City</label>
                    <input type="text" class="form-control" id="validationCustom03" name="city" bind:value={$city} required>
                    <div class="invalid-feedback">
                    Please provide a valid city.
                </div>
                </div>
                <div class="col-md-3">
                    <label for="validationCustom04" class="form-label">Vessel Name</label>
                    <input type="text" class="form-control" id="validationCustom04" name="vessel_name" bind:value={$vessel_name} required>
                    <div class="invalid-feedback">
                        Please enter a valid vessel name.
                </div>
                </div>
                <div class="col-md-3">
                    <label for="validationCustom05" class="form-label">Phone</label>
                    <input type="text" class="form-control" id="validationCustom05" name="phone" bind:value={$phone} required>
                    <div class="invalid-feedback">
                    Please provide a valid phone.
                </div>
                </div>
                <div class="col-12">
                    <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="invalidCheck" required>
                    <label class="form-check-label" for="invalidCheck">
                        Agree to terms and conditions
                    </label>
                    <div class="invalid-feedback">
                        You must agree before submitting.
                    </div>
                </div>
                </div>
                <div class="col-12">
                    <button id="createProjectBtn" class="btn btn-primary" type="submit">Create a new Project</button>
                </div>
            </form>
            <h1>Добро пожаловать!</h1>
            <h2>Ваши проекты:</h2>

            <ul>
                {#if $projects.length > 0}
                    {#each $projects as project (project._id)}
                        <li class="project-info">
                            <Link to={`/EditProject/${project._id}`}>{project._id}</Link>
                            <!--<a href="/edit_project/{project._id}" on:click={() => goToEditProject(project._id)}>Sign in</a>-->
                            <strong>Name:</strong> {project.first_name} {project.last_name}<br>
                            <strong>City: </strong> {project.city}<br>
                            <strong>Phone: </strong> {project.phone}<br>
                            <strong>Post: </strong> {project.post}<br>
                            <strong>Time create: </strong> {project.created_at}<br>
                            <p><strong>Vessel name: </strong> {project.vessel_name}</p>
                        </li>
                    {/each}
                {:else}
                    <p>У вас пока нет проектов.</p>
                {/if}
            </ul>
        <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script> -->
    </main>