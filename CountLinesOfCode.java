import java.io.File;
import java.util.Scanner;

/*
Count the number of lines of Python code in all .py files in a directory,
including all files in subdirectories.
 */
public class CountLinesOfCode {

    private static boolean isPythonFile(File file) {
        if (!file.exists()) {
            return false;
        }
        String name = file.getName();
        return name.endsWith(".py");
    }

    /*
    Return true if it is a non-blank, non-comment line of code (except that
    docstrings do count as lines of code).
     */
    private static boolean isLineOfCode(String theLine) {
        String line = theLine.trim();
        return !line.startsWith("#") && line.length() > 0;
    }

    private static int linesOfCodeIn(File file) {
        if (!isPythonFile(file)) {
            return 0;
        }
        int count = 0;
        try (Scanner scanner  = new Scanner(file)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                if (isLineOfCode(line)){
                    count += 1;
                }
            }
            System.out.println(count + " lines in " + file.getName());
        } catch (Exception e) {
            System.out.println("Error!");
            e.printStackTrace();
        }
        return count;
    }

    private static boolean isVenvDirectory(File file) {
        return file.getName().endsWith("venv");
    }

    private static int countLinesOfCodeStartingAt(File file) {
        int count = 0;
        if (file.isDirectory()) {
            if (isVenvDirectory(file)) {
                // As I am using Pycharm, I don't want to include the venv directory.
                return 0;
            }
            for (File subFile : file.listFiles()) {
                count += countLinesOfCodeStartingAt(subFile);
            }
        } else {
            count = linesOfCodeIn(file);
        }
        return count;
    }


    private static File getBaseDirectory() {
        File file = new File(".");
        if (file.exists()) {
            System.out.println("Found the directory");
        } else {
            System.out.println("Did not find the directory.");
        }
        return file;
    }

    public static void main(String[] args) {
        File baseDirectory = getBaseDirectory();
        int count = countLinesOfCodeStartingAt(baseDirectory);
        System.out.println("total: " + count);
    }
}
