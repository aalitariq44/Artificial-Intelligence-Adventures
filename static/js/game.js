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

    function updateStats(stats) {
        const healthBar = document.getElementById('health-bar');
        const reputationBar = document.getElementById('reputation-bar');

        if (healthBar && reputationBar) {
            healthBar.style.width = `${stats.health}%`;
            healthBar.textContent = `الصحة: ${stats.health}%`;
            reputationBar.style.width = `${stats.reputation}%`;
            reputationBar.textContent = `السمعة: ${stats.reputation}%`;
        }
    }

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
                storyContainer.innerHTML = `
                    <div class="stats-container mb-3">
                        <div class="progress mb-2">
                            <div id="health-bar" class="progress-bar bg-danger" style="width: 100%">
                                الصحة: 100%
                            </div>
                        </div>
                        <div class="progress">
                            <div id="reputation-bar" class="progress-bar bg-info" style="width: 50%">
                                السمعة: 50%
                            </div>
                        </div>
                    </div>
                    <p>${data.story}</p>
                `;
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

                pointsCounter.textContent = (parseInt(pointsCounter.textContent) + data.points).toString();
                choicesCounter.textContent = (parseInt(choicesCounter.textContent) + 1).toString();

                if (data.stats) {
                    updateStats(data.stats);
                }

                storyContainer.innerHTML += `
                    <div class="user-decision my-3">
                        <p class="decision-text"><strong>قرارك:</strong> ${userText}</p>
                        <div class="decision-impact">
                            <span class="badge bg-warning">+${data.points} نقطة</span>
                        </div>
                    </div>
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