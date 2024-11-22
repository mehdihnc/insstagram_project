class FollowManager {
    constructor() {
        console.log('FollowManager initialized');
        const followBtn = document.getElementById('followBtn');
        
        if (followBtn) {
            followBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                console.log('Follow button clicked');
                const userId = followBtn.dataset.userId;
                
                try {
                    const response = await fetch(`/follows/toggle/${userId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        }
                    });

                    const data = await response.json();
                    console.log('Response:', data);
                    
                    if (data.status === 'success') {
                        followBtn.textContent = data.is_following ? 'Ne plus suivre' : 'Suivre';
                        followBtn.classList.toggle('btn-primary');
                        followBtn.classList.toggle('btn-outline-primary');
                        
                        const followersCount = document.querySelector('.followers-count');
                        if (followersCount) {
                            followersCount.textContent = data.followers_count;
                        }
                    }
                } catch (error) {
                    console.error('Erreur:', error);
                }
            });
        }
    }
} 