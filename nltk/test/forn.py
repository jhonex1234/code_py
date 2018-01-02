flow = ((previous_state == 's2' and current_state == 's3' and next_state_proba > 40) or 
                        (previous_state == 's2' and current_state == 's4' and next_state_proba > 70) or
                        (previous_state == 's3' and current_state == 's4' and next_state_proba > 70))

