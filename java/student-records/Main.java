import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;

/** Desktop student-record manager. Data is stored locally in students.csv. */
public class Main {
    private static final Path DATA_FILE = Paths.get("students.csv");
    private final List<Student> students = new ArrayList<>();
    private final DefaultTableModel model = new DefaultTableModel(
            new String[]{"ID", "Name", "Course"}, 0) {
        @Override public boolean isCellEditable(int row, int column) { return false; }
    };

    private static class Student {
        final int id;
        final String name;
        final String course;
        Student(int id, String name, String course) {
            this.id = id; this.name = name; this.course = course;
        }
    }

    private Main() {
        load();
        JFrame frame = new JFrame("ABSOLAD | Student Records");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(720, 480);
        frame.setLocationRelativeTo(null);

        JPanel root = new JPanel(new BorderLayout(12, 12));
        root.setBorder(BorderFactory.createEmptyBorder(18, 18, 18, 18));
        root.add(new JLabel("STUDENT RECORDS", SwingConstants.CENTER), BorderLayout.NORTH);
        JTable table = new JTable(model);
        table.setRowHeight(26);
        root.add(new JScrollPane(table), BorderLayout.CENTER);

        JPanel actions = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 4));
        JButton add = new JButton("Add student");
        JButton search = new JButton("Search by ID");
        JButton delete = new JButton("Delete selected");
        actions.add(add); actions.add(search); actions.add(delete);
        root.add(actions, BorderLayout.SOUTH);

        add.addActionListener(event -> addStudent(frame));
        search.addActionListener(event -> searchStudent(frame));
        delete.addActionListener(event -> {
            int row = table.getSelectedRow();
            if (row >= 0) {
                students.remove(row);
                model.removeRow(row);
                save();
            } else {
                JOptionPane.showMessageDialog(frame, "Select a student first.");
            }
        });

        frame.setContentPane(root);
        refresh();
        frame.setVisible(true);
    }

    private void addStudent(Component parent) {
        try {
            String idText = JOptionPane.showInputDialog(parent, "Student ID:");
            if (idText == null) return;
            int id = Integer.parseInt(idText.trim());
            if (id <= 0 || students.stream().anyMatch(s -> s.id == id)) {
                throw new IllegalArgumentException("ID must be positive and unique.");
            }
            String name = JOptionPane.showInputDialog(parent, "Student name:");
            if (name == null) return;
            String course = JOptionPane.showInputDialog(parent, "Course:");
            if (course == null) return;
            if (name.isBlank() || course.isBlank()) {
                throw new IllegalArgumentException("Name and course are required.");
            }
            students.add(new Student(id, name.trim(), course.trim()));
            save();
            refresh();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(parent, "ID must be a whole number.");
        } catch (IllegalArgumentException ex) {
            JOptionPane.showMessageDialog(parent, ex.getMessage());
        }
    }

    private void searchStudent(Component parent) {
        String input = JOptionPane.showInputDialog(parent, "Enter student ID:");
        if (input == null) return;
        try {
            int id = Integer.parseInt(input.trim());
            Student found = students.stream().filter(s -> s.id == id).findFirst().orElse(null);
            JOptionPane.showMessageDialog(parent, found == null
                    ? "Student not found."
                    : "ID: " + found.id + "\nName: " + found.name + "\nCourse: " + found.course);
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(parent, "ID must be a whole number.");
        }
    }

    private void refresh() {
        model.setRowCount(0);
        for (Student student : students) {
            model.addRow(new Object[]{student.id, student.name, student.course});
        }
    }

    private void load() {
        if (!Files.exists(DATA_FILE)) return;
        try (BufferedReader reader = Files.newBufferedReader(DATA_FILE)) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] fields = line.split(",", -1);
                if (fields.length == 3) {
                    try {
                        students.add(new Student(Integer.parseInt(fields[0]),
                                unescape(fields[1]), unescape(fields[2])));
                    } catch (NumberFormatException ignored) {
                        System.err.println("Skipping invalid student row.");
                    }
                }
            }
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(null, "Could not load students: " + ex.getMessage());
        }
    }

    private void save() {
        try (BufferedWriter writer = Files.newBufferedWriter(DATA_FILE)) {
            for (Student student : students) {
                writer.write(student.id + "," + escape(student.name) + "," + escape(student.course));
                writer.newLine();
            }
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(null, "Could not save students: " + ex.getMessage());
        }
    }

    private static String escape(String value) {
        return value.replace("\\", "\\\\").replace(",", "\\c")
                .replace("\n", "\\n").replace("\r", "");
    }
    private static String unescape(String value) {
        return value.replace("\\n", "\n").replace("\\c", ",").replace("\\\\", "\\");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Main::new);
    }
}
