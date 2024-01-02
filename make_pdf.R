find_icon_for_weather = function(forecast, day) {
#  message("fifw")
#  message(day)
  cloudiness = forecast$cloudiness[[day]]
  precipitation = forecast$precipitation[[day]]
  wind = forecast$wind[[day]]
  tmax = forecast$temperature[[day]]
  tmin = forecast$night_temperature[[day]]
  tmean = mean(tmax, tmin)

  # Storm flag
  storm = wind == 6

  # Handle precipitation-free situation
  if (precipitation == 0) {
    if (storm) {
      return("storm1.png")
    } else {
      return(sprintf("clouds%s.png", cloudiness))
    }
  } else {
  # Decide type of precipitation.
    if (tmax < 2) {
      pp_type = "snow"
    } else if (tmean > 5) {
      pp_type = "liquid"
    } else {
      pp_type = "mixed"
      return("pp_mixed.png")
    }

    if (storm & pp_type == "liquid") {
      return("rainstorm.png")
    } else {
      return(sprintf("pp_%s%s.png", pp_type, precipitation))
    }
  }
}

append_tabular_symbol = function(text, column, n_columns) {
  if (column == n_columns) {
    next_symbol = r"(\\)"
  } else {
    next_symbol = r"(&)"
  }
  return(paste0(text, next_symbol))
}

make_text = function(weather_icons, day_temps, night_temps, wind) {
  n_columns = 10
  n_rows = 3
  tabular_format = paste0(rep("c", n_columns), collapse = "")

  day = function(row, column) {
    return(((row-1)*n_columns) + column)
  }

  text = r"()"
  for (row in 1:n_rows) {
    text = paste0(text, sprintf(r"(\begin{tabular}{%s}
                                )", tabular_format))

    #_Header_Row__________________________________________________________________
    for (column in 1:n_columns) {
      text = paste0(text, sprintf(r"(Tag %s)", day(row, column)))
      text = append_tabular_symbol(text, column, n_columns)
    }

    #_Icon_Row____________________________________________________________________
    for (column in 1:n_columns) {
      today = day(row, column)
      text = paste0(text, sprintf(r"(\includegraphics[width=1cm]{%s})", 
                                  weather_icons[[today]]))
      text = append_tabular_symbol(text, column, n_columns)
    }

    #_T_Rows______________________________________________________________________
    for (column in 1:n_columns) {
      today = day(row, column)
      text = paste0(text, r"(\multicolumn{1}{l}{)")
      text = paste0(text, sprintf(r"(\includegraphics[width=0.3cm]{%s})",
                                  "clouds0.png"))
      text = paste0(text, sprintf(r"(%s $^\circ$C})", day_temps[[today]]))
      text = append_tabular_symbol(text, column, n_columns)
    }
    for (column in 1:n_columns) {
      today = day(row, column)
      text = paste0(text, r"(\multicolumn{1}{l}{)")
      text = paste0(text, sprintf(r"(\includegraphics[width=0.3cm]{%s})",
                                  "clouds0_night.png"))
      text = paste0(text, sprintf(r"(%s $^\circ$C})", night_temps[[today]]))
      text = append_tabular_symbol(text, column, n_columns)
    }
    #_Wind_Row____________________________________________________________________
    for (column in 1:n_columns) {
      today = day(row, column)
      text = paste0(text, sprintf(r"(\includegraphics[width=1cm]{wind%s.png})",
                                  wind[[today]]))
      text = append_tabular_symbol(text, column, n_columns)
    }
    text = paste0(text, r"(
  \end{tabular}
  \\[1cm]
)")
  }
  return(text)
}

make_pdf = function(forecast) {
  # Prepare temporary working environment.
  original_wd = getwd()
  tmp = tempdir()
  tmpfilename = basename(tempfile())
  tmpdirname = file.path(tmp, sprintf("%s.d", tmpfilename))
  dir.create(tmpdirname)
  setwd(tmpdirname)
  tex = paste0(tmpfilename, ".tex")
  output_name = paste0(tmpfilename, ".pdf")

  # Start the LaTeX header.
  doc = r"(
\documentclass{article}
\usepackage{cmbright}
\usepackage[a4paper, margin=2cm]{geometry}
\usepackage{graphicx}
\graphicspath{{%s/icons/}}
\pagenumbering{gobble}
\begin{document}
\begin{center}
%s
\end{center}
\end{document}
)"
  # Create the contents.
  n_days = 30
  weather_icons = sapply(1:n_days, function(day) {
                           find_icon_for_weather(forecast, day)
  })
  day_temps = forecast$temperature
  night_temps = forecast$night_temperature
  wind = forecast$wind
  content = make_text(weather_icons, day_temps, night_temps, wind)
  # Write .tex file.
  write(sprintf(doc, original_wd, content), tex)
  # Render pdf using LaTeX.
  system(sprintf("pdflatex %s", tex))
  # Move rendered pdf over here.
  system(sprintf("cp %s %s", output_name, 
                 file.path(original_wd, "latest_output.pdf")))
  # Cleanup.
 setwd(original_wd)
  unlink(tmpdirname, recursive = TRUE)
}

