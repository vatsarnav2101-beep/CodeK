import 'package:flutter/material.dart';
import '../api.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final controller = TextEditingController();
  final api = CodeKApi();
  String output = 'Enter a coding task and press Run.';
  bool running = false;

  Future<void> runTask() async {
    final prompt = controller.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      running = true;
      output = 'Running...';
    });

    try {
      final data = await api.run(prompt);
      final results = (data['results'] as List).cast<Map<String, dynamic>>();
      final lines = <String>[
        'Plan:',
        ...(data['plan'] as List).map((item) => '- $item'),
        '',
        'Results:',
        ...results.map((item) => '[${item['status']}] ${item['task']}: ${item['result']}'),
      ];
      setState(() => output = lines.join('\n'));
    } catch (error) {
      setState(() => output = 'Error: $error');
    } finally {
      setState(() => running = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('CodeK')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: controller,
              minLines: 3,
              maxLines: 5,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Coding task',
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: running ? null : runTask,
                child: Text(running ? 'Running...' : 'Run'),
              ),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: SelectableText(output),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
