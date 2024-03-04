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
        const response = await fetch(`https://survzilla-frontend-finish.onrender.com/api/EditProject/${project_id}`, {
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/add_step`, {
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/add_section`, {
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/add_subsection`, {
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/add_imagestandard`, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    project.set(data.updated_project);
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/remove_step`, {
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
            const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/remove_image`, {
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
        
        const response = await fetch(`https://survzilla-frontend-finish.onrender.com/edit_project/${$project._id}/get-gpt-recommendations`, {
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
        const response = await fetch(`https://survzilla-frontend-finish.onrender.com/download_project_pdf/${$project._id}`);
        
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
</script>

<style>

    main {
        width: 100%;
        height: 100%;
        min-height: 100vh;
        color: rgb(255, 255, 255);
        background: linear-gradient(to bottom, #011a2b, #011529);
    }

    .top {
    display: flex;
    justify-content: space-evenly;
    margin: 15px;
    width: 92%;
}

button {
    margin: 13px;
    padding: 15px;
    border-radius: 10%;
    background-color: #d3be25f2;
}

.forplus {
    float: right;
    margin-right: 9%;
}

.forosnova {
    display: flex;
    justify-content: space-around;
}



.deck {
    margin-left: 2%;
}

.button-clicked {
    background-color: #14d424; /* Замените на желаемый цвет */
    color: rgb(141, 22, 22); /* Замените на желаемый цвет текста */
}

.subsection-button-clicked {
    background-color: #4CAF50; /* Замените на желаемый цвет */
    color: rgb(8, 5, 5); /* Замените на желаемый цвет текста */
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
    border: 1px solid #888;
    width: 50%;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

h3 {
    color: #000000;
}

.formablack {
    color: #000000;
}

img {
    max-width: 200px; /* Максимальная ширина изображения будет равна ширине контейнера */
    max-height: 150px;/* Автоматическое вычисление высоты, чтобы сохранить пропорции */
}

.footer{
    height: 570px;
}



.thumbnail {
        width: 300px; /* Или другой подходящий размер */
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
    height: 500px;
}

.subsections {
    display: flex;/* Space between each item */
}

.subsection {
    display: block;
    
}

</style>


<main>
    {#if $project}
    <h1 class="sitename">Survzilla</h1>
    <Link to="/glav" class="btn btn-danger">Выйти из проекта</Link><!-- кнопка перехода на страницу создания проектов -->
    <div class="top">
        <h1>Edit Project: { $project.first_name } { $project.last_name } vessel name: { $project.vessel_name }</h1>
    </div>
    {/if}
        <div class="deck">
        {#if $project}
        <div class="sections-buttons">
            {#each Object.keys($project.sections) as sectionKey}
                <button on:click={() => showSection(sectionKey)}>{sectionKey.toUpperCase().replace(/_/g, ' ')}</button>
            {/each}
            <button id="create-section-button" class="forplus" on:click={showCreateSectionModal}>+</button>
            <button on:click={downloadPdf}>Получить PDF</button>
        </div>

        {#if $selectedSection}
            <div class="section-content">
                <h1>{$currentSection}</h1>
                {#each Object.keys($selectedSection) as subsectionKey}
                    <button on:click={() => showSubsectionForm($currentSection, subsectionKey)}>{subsectionKey.toUpperCase().replace(/_/g, ' ')}</button>
                {/each}
                <button class="forplus" on:click={() => showCreateSubsectionModal($currentSection)}>{$currentSection}+</button>
            </div>
        {/if}
        {#if $showAddStepForm}
        <div id="add-step-form-container" >
            <h1>{$currentSubsection.toUpperCase().replace(/_/g, ' ')}</h1>
            {#if activeImage}
                <div class="modalimage" on:click={() => activeImage = null}>
                    <img src={activeImage} alt="Active Image" class="active-image"/>
                </div>
            {/if}
            {#if $project.sections[$currentSection] && $project.sections[$currentSection][$currentSubsection]}
                <div>
                    {#each $project.sections[$currentSection][$currentSubsection].images as image}
                        <img src={image} alt="Step image" class="step-image"/>
                        <button on:click={() => removeImage(image)}>Remove</button>
                    {/each}
                </div>
                <div id="step-recommendations">
                    <p>{stepRecommendations}</p>
                </div>
                <div class="steps-and-images">
                    {#each $project.sections[$currentSection][$currentSubsection].steps as step}
                        <div class="step">{step}</div>
                        <button on:click={() => removeStep(step)}>Remove</button>
                    {/each}
                </div>
            {/if}
            <form on:submit={addStep}>
                <label for="step_description">Step Description:</label>
                <input type="text" id="step_description" name="step_description">
                <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                <button type="submit">Add Step</button>
            </form>
            
            <form on:submit={addImageStandard}>
                <label for="image_upload">Select Image:</label>
                <input type="file" id="image_upload" name="image_upload">
                <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                <button type="submit">Add Image</button>
            </form>
            
            <form on:submit={getStepRecommendations}>
                <input type="hidden" name="subsection" id="current_subsection" bind:value={$currentSubsection}>
                <input type="hidden" name="section" id="current_section" bind:value={$currentSection}>
                <label for="step_description">Describe in detail:</label>
                <input type="text" name="step_description" id="step_description" value="">
                <button type="submit">Help bot</button>
            </form>
            
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
            <form on:submit={addSection}>
                <label class="formablack" for="section_name">Имя раздела:</label>
                <input type="text" name="section_name" id="section_name" required>
                <button type="submit">Name section</button>
            </form>
        </div>
    </div>
</main>