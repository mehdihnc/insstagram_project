class FollowManager {
    constructor() {
        this.setupFollowButtons();
    }

    setupFollowButtons() {
        document.querySelectorAll('.follow-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                const userId = button.dataset.userId;
                await this.toggleFollow(userId, button);
            });
        });
    }

    async toggleFollow(userId, button) {
        try {
            const response = await fetch(`/follows/toggle/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            });

            const data = await response.json();
            
            if (data.is_following) {
                button.textContent = 'Ne plus suivre';
                button.classList.replace('btn-primary', 'btn-outline-primary');
            } else {
                button.textContent = 'Suivre';
                button.classList.replace('btn-outline-primary', 'btn-primary');
            }

            // Mettre à jour le compteur de followers si on est sur la page de profil
            const followersCount = document.querySelector('.followers-count');
            if (followersCount) {
                followersCount.textContent = data.followers_count;
            }

        } catch (error) {
            console.error('Erreur lors du suivi:', error);
        }
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    new FollowManager();
});