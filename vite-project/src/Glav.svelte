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


    const createProject = async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const user_id = localStorage.getItem('user_id'); // Get user_id from localStorage

        const response = await fetch('https://survzilla-frontend-finish.onrender.com/index2', {
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
        const response = await fetch(`https://survzilla-frontend-finish.onrender.com/api/glav?user_id=${user_id}`, {
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
    
    let activeImage = null;
</script>

<style>

@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css');
    

form {
    width: 100%;

}

main {
    width: 100%;
    height: 100%;
    min-height: 100vh;
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
    margin-top: 0;
    margin-bottom: 0rem;
}



.project-info {
    display: flex;
    justify-content: space-between; /* Распределите пространство между деталями проекта и изображением */
    align-items: center; /* Центрирование элементов по вертикали */
    border: 1px solid #000; /* Граница вокруг каждого элемента списка */
    padding: 10px;
    background-color: #191d32;
    margin-bottom: 10px; /* Отступ между элементами списка */
}

.project-details {
    margin-left: 50px;/* Стили для деталей проекта */
}

.project-images {
    display: flex; /* Используйте flexbox для управления расположением элементов */
    justify-content: flex-end; /* Выравнивание элементов по правому краю */
    gap: 25px; /* Расстояние между элементами */
}

.project-image {
    /* Стили для изображения, например, размер */
    max-width: 300px; /* Максимальная ширина изображения */
    height: auto; /* Высота изображения будет пропорциональной ширине */
}


.project-image img {
    max-width: 300px; /* Максимальная ширина изображения */
    height: auto; /* Автоматическая высота сохранит пропорции изображения */
}

.thumbnail {
        width: 100px; /* Или другой подходящий размер */
        cursor: pointer;
}

.modalimage {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
}

.active-image {
    max-width: 90%;
    max-height: 90%;
    height: 400px;
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
            {#if activeImage}
            <div class="modalimage" on:click={() => activeImage = null}>
                <img src={activeImage} alt="Active Image" class="active-image"/>
            </div>
            {/if}
            <ul>
                {#if $projects.length > 0}
                    {#each $projects as project (project._id)}
                        <li class="project-info">
                            <div class="project-details">
                                <Link to={`/EditProject/${project._id}`}>
                                    <strong>Name:</strong> {project.first_name} {project.last_name}<br>
                                </Link>
                                <strong>City: </strong> {project.city}<br>
                                <strong>Phone: </strong> {project.phone}<br>
                                <strong>Post: </strong> {project.post}<br>
                                <strong>Time create: </strong> {project.created_at}<br>
                                <strong>Vessel name: </strong> {project.vessel_name}
                            </div>
                            <!--{#if project.sections.introduction.gen_info.images && project.sections.introduction.gen_info.images.length > 0}
                                <div class="project-images">
                                    {#each project.sections.introduction.gen_info.images as image}
                                        <div class="project-image">
                                            <img src={image} alt="Project Image" on:click={() => activeImage = image}/>
                                        </div>
                                    {/each}
                                </div>
                            {:else}
                                <h1></h1>
                            {/if}-->
                        </li>
                    {/each}
                {:else}
                    <p>У вас пока нет проектов.</p>
                {/if}
            </ul>
        <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script> -->

    </main>