'use client';
import { useEffect } from 'react';
import { useUser, useAuth } from '@clerk/nextjs';

export default function UserSync() {
  const { isLoaded, isSignedIn, user } = useUser();
  const { getToken } = useAuth();
  
  useEffect(() => {
    async function sync() {
      if (isLoaded && isSignedIn && user) {
        // Sync to local storage for static HTML dashboards
        localStorage.setItem('userAvatar', user.imageUrl || '');
        localStorage.setItem('userFirstName', user.firstName || '');
        localStorage.setItem('userLastName', user.lastName || '');

        try {
          const hasSynced = localStorage.getItem('clerk_synced_' + user.id);
          if (!hasSynced) {
            const token = await getToken();
            const res = await fetch('http://localhost:5000/api/auth/sync', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
              },
              body: JSON.stringify({
                email: user.primaryEmailAddress?.emailAddress,
                firstName: user.firstName,
                lastName: user.lastName
              })
            });
            if (res.ok) {
              localStorage.setItem('clerk_synced_' + user.id, 'true');
            }
          }
        } catch (error) {
          console.error('Failed to sync user with backend:', error);
        }
      }
    }
    sync();
  }, [isLoaded, isSignedIn, user, getToken]);

  return null;
}
