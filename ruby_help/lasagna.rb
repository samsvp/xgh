class Lasagna
    # defining our constant 
    EXPECTED_MINUTES_IN_OVEN=40
  
    def remaining_minutes_in_oven(minutes)
        # returns the expected minutes in oven minus the given
        # number of minutes. If the minutes spent are bigger
        # than the expected number of minutes, return 0
        return [EXPECTED_MINUTES_IN_OVEN - minutes, 0].max()
    end
  
    def preparation_time_in_minutes(layers)
         return 2 * layers
    end
  
    def total_time_in_minutes(number_of_layers: 0, actual_minutes_in_oven: 0)
        # the total time in minutes in the oven is the preparation times +
        # the time passed inside the oven
        return actual_minutes_in_oven + preparation_time_in_minutes(number_of_layers)
    end
end
  

# tests
puts Lasagna::EXPECTED_MINUTES_IN_OVEN
lasagna = Lasagna.new
puts lasagna.remaining_minutes_in_oven(50)
puts lasagna.preparation_time_in_minutes(2)
puts lasagna.total_time_in_minutes(number_of_layers: 2, actual_minutes_in_oven: 20)