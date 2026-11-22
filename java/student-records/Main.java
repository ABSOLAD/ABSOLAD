import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static class Student {
        private final int id;
        private final String name;
        private final String course;

        Student(int id, String name, String course) {
            this.id = id;
            this.name = name;
            this.course = course;
        }

        @Override
        public String toString() {
            return "ID: " + id + " | Name: " + name + " | Course: " + course;
        }
    }

    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        try (Scanner scanner = new Scanner(System.in)) {
            boolean running = true;
            while (running) {
                System.out.println("\n=== Student Records ===");
                System.out.println("1. Add student");
                System.out.println("2. List students");
                System.out.println("3. Search by ID");
                System.out.println("4. Exit");
                System.out.print("Choose: ");
                String choice = scanner.nextLine().trim();

                switch (choice) {
                    case "1" -> addStudent(scanner, students);
                    case "2" -> listStudents(students);
                    case "3" -> searchStudent(scanner, students);
                    case "4" -> running = false;
                    default -> System.out.println("Please choose 1, 2, 3 or 4.");
                }
            }
        }
        System.out.println("Goodbye!");
    }

    private static void addStudent(Scanner scanner, List<Student> students) {
        try {
            System.out.print("Student ID: ");
            int id = Integer.parseInt(scanner.nextLine().trim());
            boolean exists = students.stream().anyMatch(student -> student.id == id);
            if (exists) {
                System.out.println("That ID already exists.");
                return;
            }
            System.out.print("Name: ");
            String name = scanner.nextLine().trim();
            System.out.print("Course: ");
            String course = scanner.nextLine().trim();
            if (name.isEmpty() || course.isEmpty()) {
                System.out.println("Name and course cannot be empty.");
                return;
            }
            students.add(new Student(id, name, course));
            System.out.println("Student added.");
        } catch (NumberFormatException exception) {
            System.out.println("ID must be a whole number.");
        }
    }

    private static void listStudents(List<Student> students) {
        if (students.isEmpty()) {
            System.out.println("No student records yet.");
            return;
        }
        students.forEach(System.out::println);
    }

    private static void searchStudent(Scanner scanner, List<Student> students) {
        try {
            System.out.print("Enter ID: ");
            int id = Integer.parseInt(scanner.nextLine().trim());
            students.stream()
                    .filter(student -> student.id == id)
                    .findFirst()
                    .ifPresentOrElse(
                            System.out::println,
                            () -> System.out.println("Student not found.")
                    );
        } catch (NumberFormatException exception) {
            System.out.println("ID must be a whole number.");
        }
    }
}
