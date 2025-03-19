document.addEventListener('DOMContentLoaded', function() {
    const storyContainer = document.getElementById('story-container');
    const userInput = document.getElementById('user-input');
    const submitResponse = document.getElementById('submit-response');
    const startGame = document.getElementById('start-game');
    const newGame = document.getElementById('new-game');
    const inputContainer = document.getElementById('input-container');
    const startContainer = document.getElementById('start-container');
    const newGameContainer = document.getElementById('new-game-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');

    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.classList.remove('d-none');
        setTimeout(() => {
            errorAlert.classList.add('d-none');
        }, 5000);
    }

    function showLoading() {
        loadingSpinner.classList.remove('d-none');
    }

    function hideLoading() {
        loadingSpinner.classList.add('d-none');
    }

    async function startNewGame() {
        showLoading();
        try {
            const response = await fetch('/start-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                storyContainer.innerHTML = `<p>${data.story}</p>`;
                inputContainer.classList.remove('d-none');
                startContainer.classList.add('d-none');
                newGameContainer.classList.remove('d-none');
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('حدث خطأ أثناء بدء اللعبة. يرجى المحاولة مرة أخرى.');
        } finally {
            hideLoading();
        }
    }

    async function submitUserResponse() {
        const userText = userInput.value.trim();
        
        if (!userText) {
            showError('الرجاء إدخال نص قبل الإرسال');
            return;
        }

        showLoading();
        try {
            const response = await fetch('/continue-story', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userInput: userText })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const pointsCounter = document.getElementById('points-counter');
                const choicesCounter = document.getElementById('choices-counter');
                
                pointsCounter.textContent = data.points || '0';
                choicesCounter.textContent = data.choices_made || '0';
                
                storyContainer.innerHTML += `
                    <p class="user-response"><strong>ردك:</strong> ${userText}</p>
                    <p>${data.story}</p>
                `;
                userInput.value = '';
                storyContainer.scrollTop = storyContainer.scrollHeight;
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('حدث خطأ أثناء معالجة ردك. يرجى المحاولة مرة أخرى.');
        } finally {
            hideLoading();
        }
    }

    startGame.addEventListener('click', startNewGame);
    newGame.addEventListener('click', () => {
        storyContainer.innerHTML = '';
        startNewGame();
    });
    
    submitResponse.addEventListener('click', submitUserResponse);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitUserResponse();
        }
    });
});
