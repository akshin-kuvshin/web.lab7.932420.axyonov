// criterias

function saveSkills(skillsList) {
    const skills = [];

    const skillsListItems = skillsList.querySelectorAll(".editable-skills-list-item");
    for (const skillsListItem of skillsListItems)
        skills.push(skillsListItem.firstChild.textContent);

    localStorage.setItem("skills", JSON.stringify(skills));
}

function createSkillElement(skill, skillsList) {
    const deleteButton = document.createElement("button");
    deleteButton.className = "editable-skills-list-item-delete";
    deleteButton.textContent = "Удалить";
    deleteButton.addEventListener("click", () => {
        listItem.remove();
        saveSkills(skillsList);
    });

    const listItem = document.createElement("li");
    listItem.className = "editable-skills-list-item";
    listItem.appendChild(document.createTextNode(skill));
    listItem.appendChild(deleteButton);
    return listItem;
}

function main() {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark")
        document.body.classList.add("dark-theme");

    const themeToggler = document.getElementById("theme-toggler");
    if (themeToggler)
        themeToggler.addEventListener("click", () => {
            document.body.classList.toggle("dark-theme");
            const isDarkTheme = document.body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDarkTheme ? "dark" : "light");
        });
    else
        console.error("Элемент не найден: #theme-toggler.");



    const skillsList = document.getElementById("editable-skills-list");
    const addSkillButton = document.getElementById("add-editable-skill");
    const clearSkillsButton = document.getElementById("clear-editable-skills");
    const hideSkillsButton = document.getElementById("hide-editable-skills");

    if (!skillsList)
        console.error("Элемент не найден: #editable-skills-list.");
    else if (!addSkillButton)
        console.error("Элемент не найден: #add-editable-skill.");
    else if (!clearSkillsButton)
        console.error("Элемент не найден: #clear-editable-skills.");
    else if (!hideSkillsButton)
        console.error("Элемент не найден: #hide-editable-skills.");
    else {
        addSkillButton.addEventListener("click", () => {
            const skill = prompt("Введите новый навык:");
            if (skill === null || skill.trim() === "")
                return;

            skillsList.appendChild(createSkillElement(skill, skillsList));
            saveSkills(skillsList);
        });

        clearSkillsButton.addEventListener("click", () => {
            const skillsListItems = skillsList.querySelectorAll(".editable-skills-list-item");
            if (skillsListItems.length === 0) {
                alert("Навыки уже удалены.");
                return;
            }

            for (const skillsListItem of skillsListItems)
                skillsListItem.remove();
            saveSkills(skillsList);
        });

        hideSkillsButton.addEventListener("click", () => {
            skillsList.classList.toggle("invisible");

            const isHidden = skillsList.classList.contains("invisible");
            hideSkillsButton.textContent = (isHidden
                ? "Показать"
                : "Скрыть") + " список навыков";
            hideSkillsButton.classList.toggle("kolya");

            localStorage.setItem("isHidden", String(isHidden));
        });

        const savedSkills = JSON.parse(localStorage.getItem("skills") || "[]");
        for (const skill of savedSkills)
            skillsList.appendChild(createSkillElement(skill, skillsList));

        const isHidden = (localStorage.getItem("isHidden") || "true") === "true";
        if (isHidden) {
            skillsList.classList.add("invisible");
            hideSkillsButton.textContent = "Показать список навыков";
            hideSkillsButton.classList.add("kolya");
        }
    }



    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    const originalFetch = window.fetch;
    window.fetch = (url, options) => {
        if (url.startsWith('/api/time')) {
            const urlObject = new URL(url, window.location.origin);
            if (!urlObject.searchParams.has('timezone'))
                urlObject.searchParams.set('timezone', timeZone);
            url = urlObject;
        }
        return originalFetch(url, options);
    };



    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () =>
            navigator.serviceWorker.register('/sw.js')
                .then(registration => console.log('Service Worker registered:', registration.scope))
                .catch(error => console.error('Service Worker registration failed:', error))
        );
    }
}

main()
