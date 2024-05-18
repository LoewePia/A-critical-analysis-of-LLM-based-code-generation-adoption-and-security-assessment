package com.baseGPT;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    // Mock data
    private final Map<String, UserDetails> users = new HashMap<>();

    public CustomUserDetailsService() {
        // Mock data - replace with your actual user data retrieval logic
        users.put("user", org.springframework.security.core.userdetails.User
                .withUsername("user")
                .passwordEncoder(password -> passwordEncoder().encode("password"))
                .roles("USER").build());
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDetails user = users.get(username);
        if (user == null) {
            throw new UsernameNotFoundException("User not found with username: " + username);
        }
        return user;
    }
}

