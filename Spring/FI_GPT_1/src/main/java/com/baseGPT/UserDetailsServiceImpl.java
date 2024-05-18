package com.baseGPT;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import java.util.Collections;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Here you would typically load the user details from a real database
        // For simplicity, let's use hardcoded user details
        if ("user".equals(username)) {
            return new User("user", "$2a$10$JyR2YgDfXr9GyMJYZgr69u0iJZyNAnoUxTwvw9CXCAtIE6xMaT5Jq", Collections.emptyList());
        } else {
            throw new UsernameNotFoundException("User not found with username: " + username);
        }
    }
}

