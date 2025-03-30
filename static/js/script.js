document.addEventListener("DOMContentLoaded", function () {
    const imageUpload = document.getElementById("image-upload");
    const profileImagePreview = document.getElementById("profile-image-preview");

    if (imageUpload) {
        imageUpload.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profileImagePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    const login = document.querySelector('.small-input-container[placeholder="Write login"]');
    const email = document.querySelector('.small-input-container[placeholder="Write email"]');
    const nickname = document.querySelector('.small-input-container[placeholder="Write nickname"]');
    const password = document.querySelector('.small-input-container[placeholder="Write password"]');
    const repeatPassword = document.querySelector('.small-input-container[placeholder="Repeat password"]');

    const inputs = [
        { field: login, errorId: "login-error", validate: validateLogin },
        { field: email, errorId: "email-error", validate: validateEmail },
        { field: nickname, errorId: "name-error", validate: validateNickname },
        { field: password, errorId: "password-error", validate: validatePassword },
        { field: repeatPassword, errorId: "repeat-password-error", validate: validateRepeatPassword },
    ];

    inputs.forEach(({ field, validate }) => {
        if (field) {
            field.addEventListener("input", validate);
            field.addEventListener("blur", validate);
        }
    });

    function validateLogin() {
        checkField(login, "login-error", login.value.trim() !== "", "Login is required");
    }

    function validateEmail() {
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
        checkField(email, "email-error", isValid, "Valid email is required");
    }

    function validateNickname() {
        checkField(nickname, "name-error", nickname.value.trim() !== "", "Name is required");
    }

    function validatePassword() {
        checkField(password, "password-error", password.value.length >= 6, "Password must be at least 6 characters");
    }

    function validateRepeatPassword() {
        checkField(repeatPassword, "repeat-password-error", repeatPassword.value === password.value, "Passwords do not match");
    }

    function checkField(input, errorId, condition, message) {
        const errorElement = document.getElementById(errorId);
        if (condition) {
            errorElement.textContent = "";
            input.classList.remove("error");
        } else {
            errorElement.textContent = message;
            input.classList.add("error");
        }
    }
});




function validateNewquestion(){
    let valid = true;

    const title = document.getElementById('question-title');
    const title_error = document.getElementById('question-title-error');

    const text = document.getElementById("question-text");
    const text_error = document.getElementById("question-text-error");

    const tags = document.getElementById("tags");
    const tags_error = document.getElementById("tags-input-error");


    if (title.value.trim().length < 20){
        title_error.textContent = "Your title is shorter than 20 characters.";
        title.classList.add("error");
        valid = false;
    } else if(title.value.trim().length > 100){
        title_error.textContent = "Your title is longer than 100 characters.";
        title.classList.add("error");
        valid = false;
    } else {
        title_error.textContent = ""
        title.classList.remove("error");
    }

    if (text.value.trim().length < 20){
        text_error.textContent = "Your text is shorter than 20 characters.";
        text.classList.add("error");
        valid = false;
    } else if(text.value.trim().length > 1000){
        text_error.textContent = "Your text is longer than 1000 characters.";
        text.classList.add("error");
        valid = false;
    } else {
        text_error.textContent = ""
        text.classList.remove("error");
    }

    if (tags.value.trim().length > 60){
        tags_error.textContent = "Your tags are too long.";
        tags.classList.add("error");
        valid = false;
    } else {
        tags_error.textContent = "";
        tags.classList.remove("error");
    }


    return valid;
}


function validateAnswer(){
    let valid = true;
    const input_data = document.getElementById("answer-input");
    const error = document.getElementById("new-answer-error");

    if (input_data.value.trim().length < 40){
        error.textContent = "Your answer is shorter than 40 characters.";
        input_data.classList.add("error");
        valid = false;
    } else if(input_data.value.trim().length > 1000){
        error.textContent = "Your answer is longer than 1000 characters.";
        input_data.classList.add("error");
        valid = false;
    } else {
        error.textContent = ""
        input_data.classList.remove("error");
    }
    return valid;
}

function validateForm() {
    let valid = true;
    const loginField = document.getElementById("login");
    const passwordField = document.getElementById("password");
    const loginError = document.getElementById("login-auth-error");
    const passwordError = document.getElementById("password-auth-error");

    if (loginField.value.trim() !== "TestUser"){
        valid = false;
        loginError.textContent = "No user with this login!";
        loginField.classList.add("error");
    } else{
        loginError.textContent = "";
        loginField.classList.remove("error");
        if (passwordField.value.trim() !== "123456"){
            valid = false;
            passwordError.textContent = "Uncorrect password!";
            passwordField.classList.add("error");
        } else {
            passwordError.textContent = "";
            passwordField.classList.remove("error");
        }
    }

    return valid;
  
  }

// Находим все контейнеры с рейтингом
const ratingBoxes = document.querySelectorAll('.raiting-box');

// Перебираем каждый контейнер и добавляем обработчики событий
ratingBoxes.forEach((ratingBox) => {
    const likeButton = ratingBox.querySelector('.like-button');
    const dislikeButton = ratingBox.querySelector('.dislike-button');
    const counter = ratingBox.querySelector('.raiting-counter');

    let likeActive = false;
    let dislikeActive = false;
    let count = parseInt(counter.textContent.trim());

    // Лайк - обработчик
    likeButton.addEventListener('mouseenter', () => {
        if (!likeActive) {
            ratingBox.classList.add('green');
        }
    });
    likeButton.addEventListener('mouseleave', () => {
        if (!likeActive) {
            ratingBox.classList.remove('green');
        }
    });

    // Дизлайк - обработчик
    dislikeButton.addEventListener('mouseenter', () => {
        if (!dislikeActive) {
            ratingBox.classList.add('red');
        }
    });
    dislikeButton.addEventListener('mouseleave', () => {
        if (!dislikeActive) {
            ratingBox.classList.remove('red');
        }
    });

    // Функция для лайка
    likeButton.addEventListener('click', () => {
        if (likeActive) {
            likeActive = false;
            ratingBox.classList.remove('green');
            count--;
        } else {
            likeActive = true;
            ratingBox.classList.add('green');
            if (dislikeActive) {
                dislikeActive = false;
                ratingBox.classList.remove('red');
                count++;
            }
            count++;
        }
        updateCounter();
    });

    // Функция для дизлайка
    dislikeButton.addEventListener('click', () => {
        if (dislikeActive) {
            dislikeActive = false;
            ratingBox.classList.remove('red');
            count++;
        } else {
            dislikeActive = true;
            ratingBox.classList.add('red');
            if (likeActive) {
                likeActive = false;
                ratingBox.classList.remove('green');
                count--;
            }
            count--;
        }
        updateCounter();
    });

    // Функция обновления счетчика
    function updateCounter() {
        counter.textContent = count;
    }
});

// Проверяем, есть ли пагинатор на странице
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
const pagesContainer = document.getElementById("pages-container");

const totalPages = 30; // Общее количество страниц
let currentPage = 1;   // Текущая активная страница
const maxVisiblePages = 3; // Количество видимых страниц

// Проверка на наличие пагинатора
const isPaginatorAvailable = prevButton && nextButton && pagesContainer;

if (isPaginatorAvailable) {
    renderPages();
}

// Функция для рендеринга страниц
function renderPages() {
    if (!isPaginatorAvailable) return; // Если нет пагинатора, не рендерим

    pagesContainer.innerHTML = "";
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, Math.max(5, currentPage + 2));

    // Добавляем первую страницу, если она скрыта
    if (startPage > 1) {
        createPage(1);
        if (startPage > 2) {
            createDots();
        }
    }

    // Основные видимые страницы
    for (let i = startPage; i <= endPage; i++) {
        createPage(i, i === currentPage);
    }

    // Добавляем последнюю страницу, если она скрыта
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            createDots();
        }
        createPage(totalPages);
    }

    // Обновляем состояние кнопок "Назад" и "Вперёд"
    prevButton.classList.toggle("disabled", currentPage === 1);
    nextButton.classList.toggle("disabled", currentPage === totalPages);
}

// Функция для создания страницы
function createPage(number, isActive = false) {
    const page = document.createElement("a");
    page.href = "#";
    page.classList.add("page");
    page.textContent = number;

    if (isActive) {
        page.classList.add("active");
    }

    page.addEventListener("click", (e) => {
        e.preventDefault();
        currentPage = number;
        renderPages();
    });

    pagesContainer.appendChild(page);
}

// Функция для создания многоточия
function createDots() {
    const dots = document.createElement("span");
    dots.classList.add("dots");
    dots.textContent = "...";
    pagesContainer.appendChild(dots);
}

// Обработчик для кнопки "Назад"
if (prevButton) {
    prevButton.addEventListener("click", (e) => {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            renderPages();
        }
    });
}

// Обработчик для кнопки "Вперёд"
if (nextButton) {
    nextButton.addEventListener("click", (e) => {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            renderPages();
        }
    });
}

// Массив доступных тегов
const availableTags = [
    "HTML", "CSS", "JavaScript", "jQuery", "React", "Angular", "Vue",
    "Node.js", "PHP", "Python", "Django", "Flask", "Java", "Spring",
    "C#", ".NET", "Swift", "Kotlin", "SQL", "MongoDB", "TypeScript"
];

const tagInput = document.getElementById("tags");

if (tagInput) { // Только если инпут есть на странице
    $("#tags").autocomplete({
        source: function(request, response) {
            let currentValue = request.term;
            let lastTag = currentValue.split(',').pop().trim(); // Получаем последний введенный тег

            if (lastTag === "") return; // Если последний тег пустой — не показываем подсказки

            let filteredTags = availableTags.filter(tag => 
                tag.toLowerCase().startsWith(lastTag.toLowerCase())
            );

            response(filteredTags);
        },
        minLength: 1,
        focus: function(event, ui) {
            event.preventDefault(); // Предотвращаем замену всего текста при наведении стрелками
        },
        select: function(event, ui) {
            let currentValue = $("#tags").val();
            let tags = currentValue.split(',').map(tag => tag.trim()).filter(tag => tag !== ""); 

            if (tags.length > 0) {
                tags.pop();
            }

            if (tags.length < 3 && !tags.includes(ui.item.value)) {
                tags.push(ui.item.value);
            }

            $("#tags").val(tags.join(", ") + (tags.length < 3 ? ", " : ""));        
            event.preventDefault();
        },
        open: function() {
            let autocompleteMenu = $(".ui-autocomplete");
            let inputOffset = $("#tags").offset();
            let inputHeight = $("#tags").outerHeight();

            autocompleteMenu.css({
                "top": (inputOffset.top + inputHeight - 2) + "px",
                "left": inputOffset.left + "px"
            });
        }
    });

    tagInput.addEventListener("focus", function () {    
        initAutocomplete();
    });

    tagInput.addEventListener("input", function () {
        initAutocomplete();
    });

    tagInput.addEventListener("keyup", function(event) {
        let currentValue = tagInput.value;
        let tags = currentValue.split(',').map(tag => tag.trim()).filter(tag => tag !== "");

        if (tags.length > 3) {
            tagInput.value = tags.slice(0, 3).join(", ") + ", ";
        }
    });

    const autocompleteItems = document.getElementsByClassName('ui-autocomplete');
    for (const autocompleteItem of autocompleteItems) {
        autocompleteItem.style = 'margin-top: 10px;';
    }
}

document.querySelectorAll('.correct-button').forEach(button => {
    let correctFlag = false;
    
    button.addEventListener('click', () => {
        const checkIcon = button.querySelector('.correct-icon');

        if (correctFlag) {
            button.classList.remove("correct");
            button.textContent = "mark correct";
            button.appendChild(checkIcon); // Вернуть иконку в кнопку
            checkIcon.style.display = "none";
            correctFlag = false;
        } else {
            button.classList.add("correct");
            button.textContent = "correct";
            button.insertBefore(checkIcon, button.firstChild); // Переместить иконку в начало
            checkIcon.style.display = "block";
            correctFlag = true;
        }
    });
});