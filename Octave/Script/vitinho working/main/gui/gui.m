program.gui.handle = figure;
##program.gui.axes = axes('outerposition', [.2 0 .8 .85]);
##program.gui.current_axes = 1;
program.gui.infotext.handle = uicontrol(program.gui.handle,
  'style', 'text',
  'units', 'normalized',
  'position', [.2 .85 .8 .05],
  'string', '');

program.gui.main_panel.handle = uipanel(program.gui.handle,
  'units', 'normalized',
  'position', [0 .9 1 .1]);
program.gui.antennas_btn.handle = uicontrol(program.gui.main_panel.handle,
  'string', 'Antennas',
  'callback', @antennas_btn);
program.gui.analysis_btn.handle = uicontrol(program.gui.main_panel.handle,
  'string', 'Analysis',
  'callback', @analysis_btn);
##program.gui.optimization_btn.handle = uicontrol(program.gui.main_panel.handle,
##  'string', 'Optimization',
##  'callback', @optimization_btn);
##program.gui.parametrics_btn.handle = uicontrol(program.gui.main_panel.handle,
##  'string', 'Parametric',
##  'callback', @parametric_btn);
program.gui.results_btn.handle = uicontrol(program.gui.main_panel.handle,
  'string', 'Results',
  'callback', @results_btn);
program.gui.list_antennas_btn.handle = uicontrol(program.gui.main_panel.handle,
  'string', 'Save',
  'callback', @save_btn);
program.gui.list_antennas_btn.callback = @save_btn;
neat_horizontal_uipanel(program.gui.main_panel.handle);

program.gui.right_panel.handle = [];
antennas_btn([],[]);