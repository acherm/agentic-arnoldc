import java.io.*;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Scanner;

/**
 * Benchmark harness: runs bf_vm.main() N times inside a single JVM
 * to eliminate startup overhead and measure JIT-warmed performance.
 */
public class BenchBfVm {

    /** Reset the static _scanner_ field so bf_vm reads from fresh System.in */
    static void resetScanner() throws Exception {
        Field f = bf_vm.class.getDeclaredField("_scanner_");
        f.setAccessible(true);
        f.set(null, new Scanner(System.in));
    }

    public static void main(String[] args) throws Exception {
        int warmup = Integer.getInteger("warmup", 5);
        int runs = Integer.getInteger("runs", 20);
        String inputFile = args.length > 0 ? args[0] : null;

        if (inputFile == null) {
            System.err.println("Usage: java BenchBfVm <input_file>");
            return;
        }

        byte[] inputBytes = java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(inputFile));
        PrintStream realOut = new PrintStream(new FileOutputStream(FileDescriptor.out));
        PrintStream devNull = new PrintStream(new OutputStream() { public void write(int b) {} });
        Method m = bf_vm.class.getMethod("main", String[].class);

        // Warmup
        System.err.println("Warming up (" + warmup + " runs)...");
        for (int i = 0; i < warmup; i++) {
            System.setIn(new ByteArrayInputStream(inputBytes));
            resetScanner();
            System.setOut(devNull);
            m.invoke(null, (Object) new String[]{});
        }

        // Benchmark
        System.err.println("Benchmarking (" + runs + " runs)...");
        long[] times = new long[runs];
        for (int i = 0; i < runs; i++) {
            System.setIn(new ByteArrayInputStream(inputBytes));
            resetScanner();
            System.setOut(devNull);
            long t0 = System.nanoTime();
            m.invoke(null, (Object) new String[]{});
            long t1 = System.nanoTime();
            times[i] = t1 - t0;
        }

        // Results
        System.setOut(realOut);
        long sum = 0, min = Long.MAX_VALUE, max = 0;
        for (long t : times) {
            sum += t;
            if (t < min) min = t;
            if (t > max) max = t;
        }
        double avg = sum / (double) runs / 1_000_000.0;
        System.out.printf("Results (%d runs, after %d warmup):%n", runs, warmup);
        System.out.printf("  avg: %.2f ms%n", avg);
        System.out.printf("  min: %.2f ms%n", min / 1_000_000.0);
        System.out.printf("  max: %.2f ms%n", max / 1_000_000.0);
        for (int i = 0; i < runs; i++) {
            System.out.printf("  run %2d: %.2f ms%n", i + 1, times[i] / 1_000_000.0);
        }
    }
}
