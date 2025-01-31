from openai import version
import requests
import json
import os
import asyncio
from typing import Dict, Any
from jdoodle_executor import ExecuteCodeResponse, execute_code


def create_ada_hello_world() -> str:
    """
    Creates a simple Hello World program in ADA.
    The program follows ADA's strict syntax requirements.
    """
    return """with Ada.Text_IO;
use Ada.Text_IO;
procedure Hello is
begin
   Put_Line("Hello, World!");
end Hello;"""


def create_julia_hello_world() -> str:
    """
    Creates a simple Hello World program in Julia.
    """
    return """println("Hello, World!")"""

def create_fortran_sorting_program() -> str:
    """
    Creates a Fortran program that demonstrates array sorting.
    The program includes an example array, sorts it in ascending order,
    and prints both the original and sorted arrays.
    """
    return """program sorting
    implicit none
    integer :: numbers(6)
    integer :: i
    
    ! Initialize array
    data numbers /64, 34, 25, 12, 22, 11/
    
    ! Print original array
    print *, "Original array:"
    print *, (numbers(i), i=1,6)
    
    ! Call the bubble sort subroutine
    call bubble_sort(numbers, 6)
    
    ! Print sorted array
    print *, "Sorted array:"
    print *, (numbers(i), i=1,6)
    
contains
    subroutine bubble_sort(arr, n)
        implicit none
        integer, intent(in) :: n
        integer, dimension(n), intent(inout) :: arr
        integer :: i, j, temp
        logical :: swapped
        
        do i = 1, n-1
            swapped = .false.
            do j = 1, n-i
                if (arr(j) > arr(j+1)) then
                    ! Swap elements
                    temp = arr(j)
                    arr(j) = arr(j+1)
                    arr(j+1) = temp
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine bubble_sort
    
end program sorting"""

def create_groovy_sorting_program() -> str:
    """
    Creates a Groovy program that demonstrates array sorting.
    The program includes an example array, sorts it in ascending order,
    and prints both the original and sorted arrays.
    """
    return '''class SortingDemo {
    static void bubbleSort(int[] arr) {
        int n = arr.length
        boolean swapped
        
        for (int i = 0; i < n - 1; i++) {
            swapped = false
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap elements
                    int temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
                    swapped = true
                }
            }
            // If no swapping occurred, array is already sorted
            if (!swapped) break
        }
    }
    
    static void main(String[] args) {
        // Initialize array
        int[] numbers = [64, 34, 25, 12, 22, 11]
        
        // Print original array
        println "Original array:"
        println numbers.toList()
        
        // Sort the array
        bubbleSort(numbers)
        
        // Print sorted array
        println "\\nSorted array:"
        println numbers.toList()
    }
}'''


def create_clojure_hello_world() -> str:
    """
    Creates a simple Clojure program that prints 'Hello, World!' and adds two numbers.
    The program follows Clojure's functional programming style and syntax.
    """
    return """(ns hello
  (:gen-class))

(defn -main []
  (println "Hello, World!")
  (let [sum (+ 7 9)]
    (println "The sum of 7 and 9 is:" sum)))"""

def create_julia_hello_world2() -> str:
    """
    Creates a simple Julia program that prints 'Hello, World!' and adds two numbers.
    The program follows Julia's syntax and demonstrates basic arithmetic and printing.
    """
    return """# Print hello world
println("Hello, World!")

# Add 7 and 9 and store the result
sum = 7 + 9

# Print the result
println("The sum of 7 and 9 is: ", sum)"""

def create_clojure_hello_world2() -> str:
    """
    Creates a simple Clojure program that prints 'Hello, World!' and adds two numbers.
    The program follows Clojure's functional programming style and syntax.
    """
    return """(println "Hello, World!")
(let [sum (+ 7 9)]
  (println "The sum of 7 and 9 is:" sum))"""

def create_scala_sorting_program() -> str:
    """
    Creates a Scala program that demonstrates array sorting.
    The program includes an example array, sorts it in ascending order,
    and prints both the original and sorted arrays.
    """
    return '''object SortingDemo {
  def bubbleSort(arr: Array[Int]): Unit = {
    val n = arr.length
    
    def innerLoop(i: Int, j: Int, swapped: Boolean): Boolean = {
      if (j >= n - i - 1) swapped
      else if (arr(j) > arr(j + 1)) {
        // Swap elements
        val temp = arr(j)
        arr(j) = arr(j + 1)
        arr(j + 1) = temp
        innerLoop(i, j + 1, true)
      } else innerLoop(i, j + 1, swapped)
    }
    
    def outerLoop(i: Int): Unit = {
      if (i < n - 1) {
        val swapped = innerLoop(i, 0, false)
        if (swapped) outerLoop(i + 1)
      }
    }
    
    outerLoop(0)
  }
  
  def main(args: Array[String]): Unit = {
    // Initialize array
    val numbers = Array(64, 34, 25, 12, 22, 11)
    
    // Print original array
    println("Original array:")
    println(numbers.mkString(", "))
    
    // Sort the array
    bubbleSort(numbers)
    
    // Print sorted array
    println("\\nSorted array:")
    println(numbers.mkString(", "))
  }
}'''

def get_some_rust_code() -> str:
    return """
    use std::collections::{HashMap, HashSet};
use std::io::{self, BufRead};

#[derive(Debug)]
struct Episode {
    name: String,
    number: i32,
    reviews: Vec<i32>,
}

impl Episode {
    fn new(name: String, number: i32) -> Self {
        Episode {
            name,
            number,
            reviews: Vec::new(),
        }
    }

    // Returns the average rating of this episode. If no reviews, 0.0.
    fn average_rating(&self) -> f64 {
        if self.reviews.is_empty() {
            0.0
        } else {
            let sum: i32 = self.reviews.iter().sum();
            sum as f64 / self.reviews.len() as f64
        }
    }
}

#[derive(Debug)]
struct Series {
    name: String,
    actors: Vec<String>,
    episodes: HashMap<String, Episode>,
}

impl Series {
    fn new(name: String, actors: Vec<String>) -> Self {
        Series {
            name,
            actors,
            episodes: HashMap::new(),
        }
    }

    // Returns the average rating of the entire series. If no episodes, return None.
    fn average_rating(&self) -> Option<f64> {
        if self.episodes.is_empty() {
            return None;
        }
        let total_episodes = self.episodes.len() as f64;
        let sum: f64 = self.episodes.values().map(|ep| ep.average_rating()).sum();
        Some(sum / total_episodes)
    }
}

/// A simple parser to split a line into tokens.
fn parse_line(line: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut chars = line.chars().peekable();

    // Parse the first token (command)
    let mut first_token = String::new();
    while let Some(&c) = chars.peek() {
        if c.is_whitespace() {
            break;
        }
        first_token.push(c);
        chars.next();
    }
    if !first_token.is_empty() {
        tokens.push(first_token);
    }

    // Skip whitespace
    while let Some(&c) = chars.peek() {
        if c.is_whitespace() {
            chars.next();
        } else {
            break;
        }
    }

    // Parse remaining quoted strings or integers
    while let Some(&c) = chars.peek() {
        if c == '\"' {
            chars.next(); // consume opening quote
            let mut quoted = String::new();
            while let Some(&inner_c) = chars.peek() {
                if inner_c == '\"' {
                    chars.next();
                    break;
                }
                quoted.push(inner_c);
                chars.next();
            }
            tokens.push(quoted);
        } else {
            let mut unquoted = String::new();
            while let Some(&nc) = chars.peek() {
                if nc.is_whitespace() {
                    break;
                }
                unquoted.push(nc);
                chars.next();
            }
            tokens.push(unquoted);
        }
        
        // Skip whitespace
        while let Some(&wc) = chars.peek() {
            if wc.is_whitespace() {
                chars.next();
            } else {
                break;
            }
        }
    }
    tokens
}

fn main() -> Result<(), std::io::Error> {
    let stdin = io::stdin();
    let reader = stdin.lock();

    let mut series_map: HashMap<String, Series> = HashMap::new();
    let mut actor_to_series: HashMap<String, HashSet<String>> = HashMap::new();

    for line_result in reader.lines() {
        let line = line_result?;
        if line.trim().is_empty() {
            continue;
        }

        let tokens = parse_line(&line);
        if tokens.is_empty() {
            println!("false");
            continue;
        }

        let command = &tokens[0];

        match command.as_str() {
            "AddSeries" => {
                if tokens.len() < 2 {
                    println!("false");
                    continue;
                }
                let series_name = &tokens[1];

                if series_map.contains_key(series_name) {
                    println!("false");
                    continue;
                }

                let actors: Vec<String> = tokens[2..].to_vec();
                let s = Series::new(series_name.to_string(), actors.clone());
                series_map.insert(series_name.clone(), s);

                for actor in actors {
                    actor_to_series.entry(actor).or_insert_with(HashSet::new).insert(series_name.clone());
                }

                println!("true");
            }
            "AddEpisode" => {
                if tokens.len() < 4 {
                    println!("false");
                    continue;
                }
                let series_name = &tokens[1];
                let episode_name = &tokens[2];
                let number = match tokens[3].parse::<i32>() {
                    Ok(n) => n,
                    Err(_) => {
                        println!("false");
                        continue;
                    }
                };

                if let Some(series) = series_map.get_mut(series_name) {
                    if series.episodes.contains_key(episode_name) {
                        println!("false");
                        continue;
                    }
                    let ep = Episode::new(episode_name.clone(), number);
                    series.episodes.insert(episode_name.clone(), ep);
                    println!("true");
                } else {
                    println!("false");
                }
            }
            "AddReview" => {
                if tokens.len() < 4 {
                    println!("false");
                    continue;
                }
                let series_name = &tokens[1];
                let episode_name = &tokens[2];
                let rating = match tokens[3].parse::<i32>() {
                    Ok(r) if (1..=5).contains(&r) => r,
                    _ => {
                        println!("false");
                        continue;
                    }
                };

                if let Some(series) = series_map.get_mut(series_name) {
                    if let Some(ep) = series.episodes.get_mut(episode_name) {
                        ep.reviews.push(rating);
                        println!("true");
                    } else {
                        println!("false");
                    }
                } else {
                    println!("false");
                }
            }
            "GetSeriesRating" => {
                if tokens.len() < 2 {
                    println!("false");
                    continue;
                }
                let series_name = &tokens[1];

                if let Some(series) = series_map.get(series_name) {
                    match series.average_rating() {
                        Some(avg) => println!("{:.1}", avg),
                        None => println!("false"),
                    }
                } else {
                    println!("false");
                }
            }
            "GetSeriesByActor" => {
                if tokens.len() < 2 {
                    println!("");
                    continue;
                }
                let actor_name = &tokens[1];
                if let Some(sr) = actor_to_series.get(actor_name) {
                    let mut series_list: Vec<String> = sr.iter().cloned().collect();
                    series_list.sort();
                    println!("{}", series_list.join(","));
                } else {
                    println!("");
                }
            }
            _ => {
                println!("false");
            }
        }
    }
    Ok(())
}
    """

async def main():
    # Get the ADA source code
    ada_code = create_ada_hello_world()
    julia_code = create_julia_hello_world()
    clojure_code = create_clojure_hello_world()
    julia_code = create_julia_hello_world2()
    clojure_code = create_clojure_hello_world2()
    fortran_code = create_fortran_sorting_program()
    groovy_code = create_groovy_sorting_program()
    scala_code = create_scala_sorting_program()
    rust_code = get_some_rust_code()

    try:
        # Execute the code using the imported execute_code function
        # We specify 'ada' as the programming language and use default values for other parameters
        response: ExecuteCodeResponse = await execute_code(
            code=rust_code,
            programming_language="rust",
            version_index="5",
            input_data="\n\n     5 3 1 4 2\n    10 9 8 7 6\n",
        )

        print(f"Response: {response}")

        # Check if the execution was successful
        if response.isExecutionSuccess:
            print("Execution successful!")
            print(f"Output: {response.output}")
            print(f"CPU Time: {response.cpuTime}")
            print(f"Memory Used: {response.memory}")
        else:
            # If execution failed, print relevant error information
            print("Execution failed!")
            print(f"Status: {response.status}")
            print(f"Error Message: {response.error_message}")
            if response.compilationStatus:
                print(f"Compilation Status: {response.compilationStatus}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Run the async main function using asyncio
    asyncio.run(main())
