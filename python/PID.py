import pypidtune

# log file = C:/Users/mantto2/Documents/Trend.csv
#    init_sp_tag="Program:MainProgram.LIC201.SP",
#    init_pv_tag="Program:MainProgram.LIC201.PV",
#    init_cv_tag="Program:MainProgram.LIC201.OUT",

# pid_logger = pypidtune.PIDLogger()
# pid_logger.root.mainloop()


pid_tuner = pypidtune.PIDTuner()
pid_tuner.root.mainloop()