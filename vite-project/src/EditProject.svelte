<script>
    import { onMount } from "svelte";
    import { useParams } from "svelte-navigator";
    import { writable } from "svelte/store";
    import { Link } from "svelte-navigator";

    let project = writable(null);

    const { subscribe } = useParams();


    //Гет запрос на сервер при переходе на страницу
    // Fetch project details when the component is mounted
    onMount(() => {
        const unsubscribe = subscribe((params) => {
        const { project_id } = params;

        fetchProjectDetails(project_id);
        });

        return unsubscribe;
    });
    
    async function fetchProjectDetails(project_id) {
        try {
        const response = await fetch(`http://127.0.0.1:5000/api/EditProject/${project_id}`, {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === "success") {
            // Convert ObjectId to string in the project data
            data.project._id = String(data.project._id);
            project.set(data.project);
            } else {
            console.error("Failed to fetch project details.");
            }
        } else {
            console.error("Failed to fetch project details.");
        }
        } catch (error) {
        console.error("Error during fetch:", error);
        }
    }

    // Добавьте вывод в консоль для отслеживания переменных
    $: {
        console.log('Current Section:', currentSection);
        console.log('Current Subsection:', currentSubsection);
        console.log('Opened Subsection:', openedSubsection);
    }
    
    // Обновленная функция addStep, которая добавляет шаг и обновляет соответствующий подраздел
    async function addStep(event) {
        event.preventDefault();

        const stepDescription = document.getElementById("step_description").value;
        const currentSection = document.getElementById("current_section").value;
        const currentSubsection = document.getElementById("current_subsection").value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    section: currentSection,
                    subsection: currentSubsection,
                    step_description: stepDescription
                }),
            });

            const data = await response.json();
            console.log(data); // Можете обработать ответ от сервера здесь
            project.set(data.updated_project);
            
        } catch (error) {
            console.error('Error:', error);
        }
    }


    $: {
        console.log("Project data:", $project);
    }
    ///Добавление раздела
    async function addSection(event) {
        event.preventDefault();

        const sectionName = document.getElementById("section_name").value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_section`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `section_name=${encodeURIComponent(sectionName)}`,
            });

            if (response.ok) {
                const data = await response.json();  // Parse JSON response
                console.log("Section added successfully:", data);
                // Optionally, you can update the project data or refresh the page
                // based on your application's requirements.
                // For example, you can call a function to refresh project data.
                // refreshProjectData();
                project.set(data.updated_project);
                closeCreateSectionModal();
            } else {
                console.error("Failed to add section:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add section:", error);
        }
    }


    let subsectionName = writable('');



    async function addSubsection(sectionName) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_subsection`, {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    section_name: sectionName,
                    subsection_name: $subsectionName
                }),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.update(currentProject => {
                    // Добавление нового подраздела в локальное состояние
                        if (!currentProject.sections[sectionName]) {
                            currentProject.sections[sectionName] = {};
                        }
                        currentProject.sections[sectionName][$subsectionName] = { images: [], steps: [] };

                        // Возвращаем обновленный проект
                        return currentProject;
                    });

                    // Вызов showSection для обновления selectedSection с новым подразделом
                    showSection(sectionName);

                    closeCreateSubsectionModal();
                } else {
                    console.error("Failed to add subsection:", data.message);
                }
            } else {
                console.error("Failed to add subsection:", response.statusText);
            }
        } catch (error) {
            console.error("Error during add subsection:", error);
        }
    }
    /////////////////////////////////////////       Open close section     /////////////////////////////////////////

    ///Модальное окно для создания подразделов
    let currentSection = writable(null); // Add this variable

    function showCreateSubsectionModal(sectionName) {
        console.log("Showing modal for section:", sectionName);
        var modal = document.getElementById("createSubsectionModal");
        modal.style.display = "block";
    }

    function closeCreateSubsectionModal() {
        var modal = document.getElementById("createSubsectionModal");
        modal.style.display = "none"; // Reset the current section when closing the modal
    }

    //Модальное окно добавления раздела
    function showCreateSectionModal() {
        var modal = document.getElementById("createSectionModal");
        modal.style.display = "block";
    }

    function closeCreateSectionModal() {
        var modal = document.getElementById("createSectionModal");
        modal.style.display = "none";
    }

    
    let currentSubsection = writable(null);

    
    let openedSubsection = null;
    

    async function addImageStandard(event) {
        event.preventDefault();

        const formData = new FormData();
        const currentSection = document.getElementById("current_section").value;
        const currentSubSection = document.getElementById("current_subsection").value;
        const imageFile = document.getElementById("image_upload").files[0]; // Получаем файл из input
        console.log(currentSection)
        formData.append('section', currentSection);
        formData.append('subsection', currentSubSection);
        formData.append('image_upload', imageFile); // Добавляем файл в FormData

        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/add_imagestandard`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
                    hideAddImagesModal()
                    // Обработка успешного ответа
                } else {
                    console.error("Failed to upload image:", data.message);
                }
            } else {
                console.error("Failed to upload image:", response.statusText);
            }
        } catch (error) {
            console.error("Error during image upload:", error);
        }
    }

    async function removeStep(step) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/remove_step`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    section: $currentSection,
                    subsection: $currentSubsection,
                    step_description: step
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log(data);
            project.set(data.updated_project);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function removeImage(image) {
        try {
            // Удаление изображения из локального состояния для немедленного обновления UI
            const updatedImages = $project.sections[$currentSection][$currentSubsection].images.filter(img => img !== image);
            project.update(currentProject => {
                currentProject.sections[$currentSection][$currentSubsection].images = updatedImages;
                return currentProject;
            });

            // Затем отправка запроса на сервер для обновления данных на бэкенде
            const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/remove_image`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    image: image,
                    section: $currentSection,
                    subsection: $currentSubsection
                }),
            });

            const data = await response.json();
            console.log(data); // Обработка ответа от сервера

        } catch (error) {
            console.error('Error:', error);
        }
    }

    let stepRecommendations = '';

    async function getStepRecommendations(event) {
        event.preventDefault();
        
        const stepDescription = document.getElementById("step_description").value;
        const currentSection = document.getElementById("current_section").value;
        const currentSubsection = document.getElementById("current_subsection").value;
        stepRecommendations = 'Наш бот уже отвечает на ваш запрос подождите...';
        
        const response = await fetch(`http://127.0.0.1:5000/edit_project/${$project._id}/get-gpt-recommendations`, {
            method: 'POST',
            headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    section: currentSection,
                    subsection: currentSubsection,
                    step_description: stepDescription
                }),
            });

        if (response.ok) {
            const data = await response.json();
            stepRecommendations = data.recommendations; // Обновление переменной с рекомендациями
        } else {
            console.error('Ошибка при получении рекомендаций');
        }
    }

    let activeImage = null;

    async function downloadPdf() {
        const response = await fetch(`http://127.0.0.1:5000/download_project_pdf/${$project._id}`);
        
        if (!response.ok) {
            alert('Произошла ошибка при загрузке PDF');
            return;
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = "project_report.pdf"; // Название файла
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
    }

    let selectedSection = writable(null);
    let showAddStepForm = writable(false);

    function showSection(sectionKey) {
        selectedSection.set($project.sections[sectionKey]);
        currentSection.set(sectionKey);
        currentSubsection.set('');
        showAddStepForm.set(false);
    }

    function showSubsectionForm(sectionKey, subsectionKey) {
        console.log('currentSection before set:', currentSection);
        currentSection.set(sectionKey);
        console.log('currentSection after set:', currentSection);
        currentSubsection.set(subsectionKey);
        showAddStepForm.set(true);
        stepRecommendations='';
    }

    function showAddImagesModal() {
    let modal = document.getElementById('addImageModal');
    modal.style.display = 'block';
    }

    function hideAddImagesModal() {
    let modal = document.getElementById('addImageModal');
    modal.style.display = 'none';
    }
</script>

<style>
    main {
        background: #1e1e1e;
        height: 1370px;
    }
.project-details {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 20px;
    justify-content: center;
    flex-direction: column;
    margin-left: 5%;
    margin-right: 5%;
  }
  
  .project-details h1 {
    font-size: 1.5em;
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
    color: #ddd7d7;
  }
  
  .section-button {
    font-size: 1em;
    padding: 10px 20px;
    margin: 5px;
    background: none;
    border: none;
    color: #ddd7d7;
    cursor: pointer;
    transition: all 0.1s ease;
    font-size: 20px;
  }
  
  .section-button:hover {
    color: #0056b3;
  }
  
  .selected-section {
    font-size: 1.2em;
    color: #0056b3;
    border-bottom: 2px solid #0056b3;
    padding-bottom: 5px;
    margin-bottom: 20px;
  }
  
    .layout-container {
        display: grid;
        grid-template-columns: 2fr 1fr;
        grid-template-rows: auto 1fr;
        gap: 20px;
        margin: 20px;
        height: calc(90vh - 40px);
    }
  
    .images-section, .steps-section, .chat-section {
      background: #f7f7f7;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
  
    .images-section {
      grid-row: 1;
      grid-column: 1 / -1;
      display: flex;
      overflow-x: auto;
      justify-content: space-between;
      background: #2a2c31;
    }
  
    .project-image {
      flex: none;
      width: 200px;
      height: auto;
      margin-right: 10px;
      border-radius: 4px;
    }
  
    .steps-section {
      grid-row: 2;
      grid-column: 1;
      display: flex;
      flex-direction: column;
      background: #2a2c31;
      color: #ddd7d7;
      overflow-x: hidden;
    }

    .steps-section .steps-list ol {
    padding: 0;
    list-style-position: inside;
    }

    .steps-section .steps-list li {
    word-wrap: break-word; /* This will break long words if needed */
    margin-bottom: 5px; /* Space between list items */
    }
  
    .steps-list {
        flex-grow: 1;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
  
    ol {
      margin: 0;
      padding-left: 20px;
    }
  
    li {
    background: #2a2c31;
      margin-bottom: 10px;
      padding: 10px;
      border-radius: 4px;
      list-style-type: decimal;
    }
  
    .add-step-form, .add-chat-form {
      display: flex;
      margin-top: 10px;
    }
  
    .add-step-form input, .add-chat-form input {
      flex-grow: 1;
      margin-right: 10px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  
    .add-step-form button, .add-chat-form button {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    .chat-section {
      grid-row: 2;
      grid-column: 2;
      display: flex;
      flex-direction: column;
      background: #2a2c31;
      color: #ddd7d7;
    }
  
    .chat-messages {
      flex-grow: 1;
      overflow-y: auto;
      color: #ddd7d7;
    }
  
    .empty-section {
      color: #999999;
      text-align: center;
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
    background: #2a2c31;
    color: white;
    margin: 10% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 50%;
    height: 20%;
    font-size: 26px;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.deliteremove {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}

.deliteimages {
    border: none;
    background: #2a2c31;
    color: white;
    cursor: pointer;
}

.lidelite {
    
}

.qwerty {
    display: flex;
    flex-direction: row-reverse;
}

.toptop {
    display: flex;
    align-items: center;
    gap: 40%;
    color: #ddd7d7;
}

.nameprojectanvessel {
    display: flex;
    justify-content: center;
    color: #ddd7d7;
    margin: 0px;
}

.sitename {
    color: #ddd7d7;
    margin: 10px;
}

.addimages {
    background: #2a2c31;
    color: white;
    border: none;
}

.forplus {
    background: #1e1e1e;
    color: white;
    font-size: 20px;
    border: none;
    cursor: pointer;
}
</style>


<main>
    {#if $project}
    <div class="toptop">
        <Link to="/glav" class="btn btn-danger">Выйти из проекта</Link><!-- кнопка перехода на страницу создания проектов -->
        <h1 class="sitename">Survzilla</h1>
    </div>
    <div class="top">
        <h1 class="nameprojectanvessel">Edit Project: { $project.first_name } { $project.last_name } vessel name: { $project.vessel_name }</h1>
    </div>
    {/if}
    <div class="project-details">
    {#if $project}
    <div class="sections-buttons">
        {#each Object.keys($project.sections) as sectionKey}
            <button class="section-button { $currentSection === sectionKey ? 'selected-section' : '' }" on:click={() => showSection(sectionKey)}>{sectionKey.toUpperCase().replace(/_/g, ' ')}</button>
        {/each}
        <button id="create-section-button" class="forplus" on:click={showCreateSectionModal}>Add Section</button>
        <button class="forplus" on:click={downloadPdf}>PDF</button>
    </div>

        {#if $selectedSection}
            <div class="subsection-details">
                <h1>{$currentSection.toUpperCase()}</h1>
                {#each Object.keys($selectedSection) as subsectionKey}
                    <button class="section-button { $currentSubsection === subsectionKey ? 'selected-section' : '' }" on:click={() => showSubsectionForm($currentSection, subsectionKey)}>{subsectionKey.toUpperCase().replace(/_/g, ' ')}</button>
                {/each}
                <button class="forplus" on:click={() => showCreateSubsectionModal($currentSection)}>Add Subsection</button>
            </div>
        {/if}
        {#if $showAddStepForm}
        <h1>{$currentSubsection.toUpperCase().replace(/_/g, ' ')}</h1>
        <div class="layout-container" >
            {#if activeImage}
                <div class="images-section" on:click={() => activeImage = null}>
                    <img  src={activeImage} alt="Active Image" class="project-image"/>
                </div>
            {/if}
            {#if $project.sections[$currentSection] && $project.sections[$currentSection][$currentSubsection]}
                <div class="images-section">
                    {#each $project.sections[$currentSection][$currentSubsection].images as image}
                        <div class="deliteremove">
                            <img src={image} alt="Step image" class="project-image"/>
                            <button class="deliteimages" on:click={() => removeImage(image)}>&times;</button>
                        </div>
                    {:else}
                        <p class="empty-section">No images available.</p>
                    {/each}
                    <div>
                        <button on:click={showAddImagesModal} class="addimages">Add images</button>
                    </div>
                </div>
                <div class="steps-section">
                    <h3>Description</h3>
                    <div class="steps-list">
                        <ol>
                        {#each $project.sections[$currentSection][$currentSubsection].steps as step}
                        <div>
                            <div class="qwerty">
                                <button class="deliteimages" on:click={() => removeStep(step)}>&times;</button>
                            </div>
                            <li class="lidelite">{step}</li>
                        </div>
                    {:else}
                        <p class="empty-section">No steps provided.</p>
                    {/each}
                        </ol>
                    <div class="add-step-form">
                        <form on:submit={addStep}>
                            <label for="step_description">Step Description:</label>
                            <input type="text" id="step_description" name="step_description">
                            <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                            <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                            <button type="submit">Add Step</button>
                        </form>
                    </div>
                    </div>
                </div>
            {/if}
            <div class="chat-section">
                <h3>Chat with Help Bot</h3>
                <!-- Your chat content goes here -->
                <div class="chat-messages">
                    <p>{stepRecommendations}</p>
                    <!-- Dynamically loaded chat messages -->
                </div>
                <div class="add-chat-form">
                    <form on:submit={getStepRecommendations}>
                        <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                        <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                        <label for="step_description">Describe in detail:</label>
                        <input type="text" name="step_description" id="step_description" value="">
                        <button type="submit">Help bot</button>
                    </form>
                </div>
            </div>
            
            <div id="addImageModal" class="modal">
                <!-- Modal content -->
                <div class="modal-content">
                    <span class="close" on:click={hideAddImagesModal}>&times;</span>
                    <form on:submit={addImageStandard}>
                        <label for="image_upload">Select Image:</label>
                        <input type="file" id="image_upload" name="image_upload">
                        <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                        <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                        <button type="submit">Add Image</button>
                    </form>
                </div>
            </div>
            
            
            
        </div>
        {/if}
    {/if}

        <!--добавление подраздела-->
        <div id="createSubsectionModal" class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => closeCreateSubsectionModal()}>&times;</span>
                <h3 class="formablack" color="black">Create New Subsection</h3>
                <form on:submit|preventDefault={() => addSubsection($currentSection)}>
                    <label class="formablack" for="subsection_name">Имя подраздела:</label>
                    <input type="text" id="subsection_name" bind:value={$subsectionName} required>
                    <button class="formablack" type="submit">Добавить подраздел</button>
                </form>
            </div>
        </div>

    <!--Модальное окно добавления раздела-->
    <div id="createSectionModal" class="modal">
        <div class="modal-content">
            <span class="close" on:click={closeCreateSectionModal}>&times;</span>
            <h3 class="formablack" color="black">Create New Section</h3>
            <div class="wasddqweqw">
                <form on:submit={addSection}>
                    <label class="formablack" for="section_name">Имя раздела:</label>
                    <input type="text" name="section_name" id="section_name" required>
                    <button type="submit">Name section</button>
                </form>
            </div>
        </div>
    </div>
</main>