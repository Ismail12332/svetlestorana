<script>
    export let webAuth;

    import { writable,derived } from 'svelte/store';
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
    let allProjects = writable([]);

    let userName = '';
    let userAvatar = '';
    let userId;

    $: {
        userName = localStorage.getItem('user_name') || 'User';
        userAvatar = localStorage.getItem('user_avatar');
    }

    onMount(() => {
        setTimeout(() => {
            fetchProjects();
            userName = localStorage.getItem('user_name') || 'User';
            userAvatar = localStorage.getItem('user_avatar');
        }, 500); // Небольшая задержка перед вызовом fetchProjects
        });
    

    const createProject = async (event) => {
        event.preventDefault(); // Prevent the default form submission
        const form = event.target; // Получаем ссылку на форму
        const accessToken = localStorage.getItem('accessToken');

        const response = await fetch('http://127.0.0.1:5000/index2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
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
                const createdAt = new Date().toLocaleString(); // Преобразуем время создания в удобный для чтения формат
                // Update the projects store with the newly created project
                projects.update(existingProjects => [...existingProjects, {
                    _id: data.project_id,
                    first_name: $first_name,
                    last_name: $last_name,
                    city: $city,
                    phone: $phone,
                    post: $post,
                    vessel_name: $vessel_name,
                    created_at: createdAt,
                    user_id: data.user_id,
                }]);
                // Notify the parent component about the successful project creation
                dispatch('projectCreated', { project_id: data.project_id });
                form.reset(); // Сбрасываем форму после успешной отправки
            } else {
                console.error('Failed to create project.');
            }
        } else {
            console.error('Failed to create project.');
            if (response.status === 401) {
                // Если токен недействителен, вызвать повторную аутентификацию
                webAuth.authorize();
            }
        }
    };
    
    //const logout = () => {
    //    localStorage.removeItem('user_id');
    //    isLoggedIn = false;
    //};


    const fetchProjects = async () => {
        const user_id = localStorage.getItem('user_id');
        const accessToken = localStorage.getItem('accessToken');
        // Send a GET request to fetch projects
        const response = await fetch(`http://127.0.0.1:5000/api/glav?user_id=${user_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Set the projects store with the fetched projects
                projects.set(data.projects);
                allProjects.set(data.projects);
                console.log(data.projects)
            } else {
                console.error('Failed to fetch projects.');
            }
        } else {
            console.error('Failed to fetch projects.');
            if (response.status === 401) {
                // Если токен недействителен, вызвать повторную аутентификацию
                webAuth.authorize();
            }
        }
    };

    // Fetch projects when the component is mounted
    
    let activeImage = null;
    let currentPage = writable(1);
    let projectsPerPage = 4;

    // Derived store to calculate paginated projects
    let paginatedProjects = derived(
        [projects, currentPage],
        ([$projects, $currentPage]) => {
        const start = ($currentPage - 1) * projectsPerPage;
        const end = start + projectsPerPage;
        return $projects.slice(start, end);
        }
    );

    let filteredProjects = writable([]);
    let searchField = ''; // начальное значение для поля поиска
    let searchQuery = '';
    let startDate = '';
    let endDate = '';

    function filterProjects() {
        const startDateObj = startDate ? new Date(startDate) : new Date('1970-01-01');
        let endDateObj = endDate ? new Date(endDate) : new Date();

        // Установка времени endDateObj на конец дня
        endDateObj.setHours(23, 59, 59, 999);

        // Получаем данные из allProjects и фильтруем их
        allProjects.subscribe(allProjectsData => {
            const filteredProjectsData = allProjectsData.filter(project => {
            const fieldMatch = !searchQuery || (project[searchField] && project[searchField].toString().toLowerCase().includes(searchQuery.toLowerCase()));

            const createdDate = new Date(project.created_at);
            const dateMatch = createdDate >= startDateObj && createdDate <= endDateObj;

            return fieldMatch && dateMatch;
            });

            // Обновляем projects отфильтрованными данными
            projects.set(filteredProjectsData);
        });
    }

    // При нажатии на кнопку поиска, обновите отфильтрованные проекты
    function onSearchClick() {
        filterProjects();
    }


    let showModal = writable(false);
    let selectedImage = writable('');

    function openImage(image) {
        selectedImage.set(image);
        showModal.set(true);
    }

    function closeImage() {
        showModal.set(false);
    }
</script>

<style>
    
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

main {
  height: 953px;
  background: #1e1e1e;
  color: white;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row-reverse;
}

.header h1 {
  font-size: 24px;
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-profile span {
  margin-right: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #fff;
}

.main-content {
  display: flex;
  height: calc(100% - 60px); /* Height of header is 60px */
  flex-direction: column;
}

.sidebar {
  min-width: 200px;
  padding: 20px;
  border-right: 1px solid #444;
}

.project-area {
  flex-grow: 1;
  padding: 20px;
}

.create-btn {
  display: flex;
  flex-direction: row-reverse;
}

.btn-create {
  padding: 10px 20px;
  margin-bottom: 20px;
  background: #0056b3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-create:hover {
  background: #004a9f;
}

.no-projects {
  color: #aaa;
}

.search-projects {
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background: #2c2c2c;
  border: 1px solid #444;
  border-radius: 4px;
  color: white;
  outline: none;
}

.search-projects::placeholder {
  color: #888;
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.search-containers {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  grid-gap: 20px;
  border-bottom: 1px solid #444;
  padding: 10px;
}

.search-input, .search-field, .date-input, .search-btn {
  padding: 10px;
  border: 1px solid #100e0e;
  border-radius: 4px;
  color: white;
  background: #2c2c2c;
  outline: none;
}

.search-btn {
  background: #282b2f;
  cursor: pointer;
}

.search-btn:hover {
  background: #004a9f;
}

.project-details {
  
}

.project-info {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
  background: #2a2c31;
  border-radius: 8px;
  overflow: hidden;
  height: 160px;
  justify-content: space-between;
}

.project-info:hover {
  background: #333740;
}

.project-details {
  padding: 1rem;
  color: #ffffff;
  flex: 1; /* Allows the details to fill the remaining space next to the images */
}

.project-details strong {
  color: #4fa1f3;
}

.no-projects {
  color: #aaaaaa;
  text-align: center;
  padding: 2rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  gap: 70px;
  margin-left: 250px;
}

.pagination-controls button {
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  background: #2a2c31;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-controls button:hover {
  background: #333740;
}

.project-images {
  display: flex;
  max-height: 200px;
}

.project-image {
  width: 220px; /* Adjust as necessary */
  height: 130px; /* Adjust as necessary */
  margin: 1.0rem;
  object-fit: cover;
  border-radius: 5px;
}

.create_project {
  display: flex;
  flex-direction: row-reverse;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
    background-color: #fff;
    margin: 10% auto;
    padding: 20px;
    border: 1px solid #2b2525;
    width: 50%;
    background: linear-gradient(to bottom, #2d2d2d, #020202);
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

#createProjectForm {
  max-width: 325px;
  margin: 0 auto;
  padding: 2rem;
  background: linear-gradient(to bottom, #212121, #232222);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#createProjectForm h2 {
  margin-bottom: 1rem;
  text-align: center;
  color: #ddd7d7;
}

#createProjectForm input[type="text"],
#createProjectForm input[type="email"],
#createProjectForm input[type="tel"] {
  width: calc(100% - 20px); /* Full width minus padding */
  padding: 10px;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

#createProjectForm input[type="text"]:focus,
#createProjectForm input[type="email"]:focus,
#createProjectForm input[type="tel"]:focus {
  border-color: #a4d7f5;
  outline: none;
}

#createProjectForm .submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #14171a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

#createProjectForm .submit-btn:hover {
  background-color: #004a9f;
}

#createProjectForm .submit-btn:active {
  transform: translateY(2px);
}

.top {
  margin-top: 14px;
}

.projectbottom {
  display: flex;
}

.surv {
  margin-right: 320px;
}



:global(a) {
  text-decoration: none;
  color: inherit;
}

.modal {
    display: block; /* Hidden by default */
    position: fixed;
    z-index: 1;
    padding-top: 100px;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 55%;
  }

  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }

  .modal-image {
    width: 100%;
  }
</style>

<!-- <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
</head> -->

<main>
<div class="main-content">
    <div class="sidebar">
      <div class="header">
        
        <div class="user-profile">
            <span>{userName}</span>
            {#if userAvatar}
                <img src={userAvatar} alt="User Avatar" class="user-avatar"/>
            {:else}
                <div class="user-avatar-placeholder"></div>
            {/if}
        </div>
      </div>
      <div class="search-containers">
        <div class="surv">
            <h1>SURVZILLA</h1>
        </div>
        <input type="text" id="searchInput" class="search-input" placeholder="Search projects..." bind:value={searchQuery}>
        <select id="searchField" class="search-field" bind:value={searchField}>
            <option value="first_name">First name</option>
            <option value="last_name">Last name</option>
            <option value="phone">Phone</option>
            <option value="city">City</option>
            <option value="email">Email</option>
            <option value="vessel_name">Vessel Name</option>
        </select>
        <label for="startDatet">Since</label>
        <input type="date" id="startDate" class="date-input" bind:value={startDate}>
        <label for="by">By</label>
        <input type="date" id="endDate" class="date-input" bind:value={endDate}>
        <button id="searchBtn" class="search-btn" on:click={onSearchClick}>Search</button>
      </div>
    </div>
    <div class="projectbottom">
      <div class="sidebar">
        <div class="search-container">
            <form id="createProjectForm" method="POST"  novalidate on:submit={createProject}>
                <h2>Create Project</h2>
                <input type="text" id="firstName" name="firstName" placeholder="First Name" bind:value={$first_name} required>
                <input type="text" id="lastName" name="lastName" placeholder="Last Name" bind:value={$last_name} required>
                <input type="email" id="email" name="email" placeholder="Email" bind:value={$post} aria-describedby="inputGroupPrepend" required>
                <input type="tel" id="phone" name="phone" placeholder="Phone" bind:value={$phone} required>
                <input type="text" id="vesselName" name="vesselName" placeholder="Vessel Name" bind:value={$vessel_name} required>
                <input type="text" id="city" name="city" placeholder="City" bind:value={$city} required>
                <button type="submit" class="submit-btn">Submit</button>
            </form>
        </div>
    </div>
    <div class="project-area">
        <ul>
          {#if $paginatedProjects.length > 0}
            {#each $paginatedProjects as project}
              <li class="project-info">
                <Link to={`/EditProject/${project._id}`}>
                <div class="project-details">
                        <strong>First Name:</strong> {project.first_name}<br>
                        <strong>Last Name:</strong> {project.last_name}<br>
                        <strong>City: </strong> {project.city}<br>
                        <strong>Phone: </strong> {project.phone}<br>
                        <strong>Post: </strong> {project.post}<br>
                        <strong>Time create: </strong> {project.created_at}<br>
                        <strong>Vessel name: </strong> {project.vessel_name}<br>
                    
                </div>
                </Link>
                <div class="project-images">
                    {#if Array.isArray(project.sections?.introduction?.gen_info?.images) && project.sections.introduction.gen_info.images.length > 0}
                      <div class="project-images">
                        {#each project.sections.introduction.gen_info.images as image}
                          <img
                            src={image}
                            alt={`Image for ${project.vessel_name}`}
                            class="project-image"
                            on:click={() => openImage(image)}
                          />
                        {/each}
                      </div>
                    {:else}
                      <p></p>
                    {/if}
                  </div>
              </li>
            {/each}
          {:else}
            <p class="no-projects">There are no projects</p>
          {/if}
        </ul>
      </div>
    </div>
    {#if $showModal}
    <div class="modal" on:click={closeImage}>
        <div class="modal-content" on:click|stopPropagation>
        <span class="close" on:click={closeImage}>&times;</span>
        <img src={$selectedImage} alt="Selected Image" class="modal-image"/>
        </div>
    </div>
    {/if}
    <div class="pagination-controls">
      <button on:click={() => currentPage.update(n => n > 1 ? n - 1 : n)}>Before</button>
      <button on:click={() => currentPage.update(n => n)}>{$currentPage}</button>
      <button on:click={() => currentPage.update(n => n + 1)}>Next</button>
    </div>
  </div>
</main>