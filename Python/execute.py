'''
A 'smoke test' for the ogusa package. Uses a fake data set to run the
baseline
'''

import cPickle as pickle
import os
import numpy as np
import time

import ogusa
ogusa.parameters.DATASET = 'REAL'


def runner(output_base, baseline_dir, baseline=False, analytical_mtrs=True, age_specific=False, reform={}, user_params={}, guid='', run_micro=True):

    #from ogusa import parameters, wealth, labor, demographics, income
    from ogusa import parameters, demog, income, utils
    from ogusa import txfunc

    tick = time.time()

    #Create output directory structure
    saved_moments_dir = os.path.join(output_base, "Saved_moments")
    ss_dir = os.path.join(output_base, "SS")
    tpi_dir = os.path.join(output_base, "TPI")
    dirs = [saved_moments_dir, ss_dir, tpi_dir]
    for _dir in dirs:
        try:
            print "making dir: ", _dir
            os.makedirs(_dir)
        except OSError as oe:
            pass

    if run_micro:
        txfunc.get_tax_func_estimate(baseline=baseline, analytical_mtrs=analytical_mtrs, age_specific=age_specific, 
                                     start_year=user_params['start_year'], reform=reform, guid=guid)
    print ("in runner, baseline is ", baseline)
    run_params = ogusa.parameters.get_parameters(baseline=baseline, guid=guid)
    run_params['analytical_mtrs'] = analytical_mtrs

    # Modify ogusa parameters based on user input
    if 'frisch' in user_params:
        print "updating fricsh and associated"
        b_ellipse, upsilon = ogusa.elliptical_u_est.estimation(user_params['frisch'],
                                                               run_params['ltilde'])
        run_params['b_ellipse'] = b_ellipse
        run_params['upsilon'] = upsilon
        run_params.update(user_params)

    # Modify ogusa parameters based on user input
    if 'g_y_annual' in user_params:
        print "updating g_y_annual and associated"
        g_y = (1 + user_params['g_y_annual'])**(float(ending_age - starting_age) / S) - 1
        run_params['g_y'] = g_y
        run_params.update(user_params)


    from ogusa import SS, TPI

    
    calibrate_model = False
    # List of parameter names that will not be changing (unless we decide to
    # change them for a tax experiment)

    param_names = ['S', 'J', 'T', 'BW', 'lambdas', 'starting_age', 'ending_age',
                'beta', 'sigma', 'alpha', 'nu', 'Z', 'delta', 'E',
                'ltilde', 'g_y', 'maxiter', 'mindist_SS', 'mindist_TPI',
                'analytical_mtrs', 'b_ellipse', 'k_ellipse', 'upsilon',
                'chi_b_guess', 'chi_n_guess','etr_params','mtrx_params',
                'mtry_params','tau_payroll', 'tau_bq',
                'retire', 'mean_income_data', 'g_n_vector',
                'h_wealth', 'p_wealth', 'm_wealth',
                'omega', 'g_n_ss', 'omega_SS', 'surv_rate', 'e', 'rho']

    '''
    ------------------------------------------------------------------------
        Run SS 
    ------------------------------------------------------------------------
    '''

    sim_params = {}
    for key in param_names:
        sim_params[key] = run_params[key]

    sim_params['output_dir'] = output_base
    sim_params['run_params'] = run_params

    income_tax_params, ss_parameters, iterative_params, chi_params = SS.create_steady_state_parameters(**sim_params)

    ss_outputs = SS.run_SS(income_tax_params, ss_parameters, iterative_params, chi_params, baseline, 
                                     baseline_dir=baseline_dir)

    '''
    ------------------------------------------------------------------------
        Pickle SS results 
    ------------------------------------------------------------------------
    '''
    if baseline:
        utils.mkdirs(os.path.join(baseline_dir, "SS"))
        ss_dir = os.path.join(baseline_dir, "SS/SS_vars.pkl")
        pickle.dump(ss_outputs, open(ss_dir, "wb"))
    else:
        utils.mkdirs(os.path.join(output_dir, "SS"))
        ss_dir = os.path.join(output_dir, "SS/SS_vars.pkl")
        pickle.dump(ss_outputs, open(ss_dir, "wb"))


    '''
    ------------------------------------------------------------------------
        Run the baseline TPI simulation
    ------------------------------------------------------------------------
    '''

    sim_params['input_dir'] = output_base
    sim_params['baseline_dir'] = baseline_dir
    

    income_tax_params, tpi_params, iterative_params, initial_values, SS_values = TPI.create_tpi_params(**sim_params)

    w_path, r_path, T_H_path, BQ_path, Y_path = TPI.run_TPI(income_tax_params, 
        tpi_params, iterative_params, initial_values, SS_values, output_dir=output_base)


    print "getting to here...."
    TPI.TP_solutions(w_path, r_path, T_H_path, BQ_path, **ss_outputs)
    print "took {0} seconds to get that part done.".format(time.time() - tick)


def runner_SS(output_base, baseline_dir, baseline=False, analytical_mtrs=True, age_specific=False, reform={}, user_params={}, guid='', run_micro=True):

    from ogusa import parameters, demographics, income, utils
    from ogusa import txfunc

    tick = time.time()

    #Create output directory structure
    saved_moments_dir = os.path.join(output_base, "Saved_moments")
    ss_dir = os.path.join(output_base, "SS")
    tpi_dir = os.path.join(output_base, "TPI")
    dirs = [saved_moments_dir, ss_dir, tpi_dir]
    for _dir in dirs:
        try:
            print "making dir: ", _dir
            os.makedirs(_dir)
        except OSError as oe:
            pass

    if run_micro:
        txfunc.get_tax_func_estimate(baseline=baseline, analytical_mtrs=analytical_mtrs, age_specific=age_specific, 
                                     start_year=user_params['start_year'], reform=reform, guid=guid)
    print ("in runner, baseline is ", baseline)
    run_params = ogusa.parameters.get_parameters(baseline=baseline, guid=guid)
    run_params['analytical_mtrs'] = analytical_mtrs

    # Modify ogusa parameters based on user input
    if 'frisch' in user_params:
        print "updating fricsh and associated"
        b_ellipse, upsilon = ogusa.elliptical_u_est.estimation(user_params['frisch'],
                                                               run_params['ltilde'])
        run_params['b_ellipse'] = b_ellipse
        run_params['upsilon'] = upsilon
        run_params.update(user_params)

    # Modify ogusa parameters based on user input
    if 'g_y_annual' in user_params:
        print "updating g_y_annual and associated"
        g_y = (1 + user_params['g_y_annual'])**(float(ending_age - starting_age) / S) - 1
        run_params['g_y'] = g_y
        run_params.update(user_params)

    from ogusa import SS, TPI

    '''
    ****
    CALL CALIBRATION here if boolean flagged

    ****
    '''
    calibrate_model = False
    # if calibrate_model:
    #     chi_b, chi_n = calibrate.(income_tax_params, ss_params, iterative_params, chi_params, baseline, 
    #                                  calibrate_model, output_dir=output_base, baseline_dir=baseline_dir)



    # List of parameter names that will not be changing (unless we decide to
    # change them for a tax experiment)

    param_names = ['S', 'J', 'T', 'BW', 'lambdas', 'starting_age', 'ending_age',
                'beta', 'sigma', 'alpha', 'nu', 'Z', 'delta', 'E',
                'ltilde', 'g_y', 'maxiter', 'mindist_SS', 'mindist_TPI',
                'analytical_mtrs', 'b_ellipse', 'k_ellipse', 'upsilon',
                'chi_b_guess', 'chi_n_guess','etr_params','mtrx_params',
                'mtry_params','tau_payroll', 'tau_bq',
                'retire', 'mean_income_data', 'g_n_vector',
                'h_wealth', 'p_wealth', 'm_wealth',
                'omega', 'g_n_ss', 'omega_SS', 'surv_rate', 'e', 'rho']


    '''
    ------------------------------------------------------------------------
        Run SS 
    ------------------------------------------------------------------------
    '''

    sim_params = {}
    for key in param_names:
        sim_params[key] = run_params[key]

    sim_params['output_dir'] = output_base
    sim_params['run_params'] = run_params

    income_tax_params, ss_params, iterative_params, chi_params= SS.create_steady_state_parameters(**sim_params)

    ss_outputs = SS.run_SS(income_tax_params, ss_params, iterative_params, chi_params, baseline, 
                                     baseline_dir=baseline_dir)

    '''
    ------------------------------------------------------------------------
        Pickle SS results 
    ------------------------------------------------------------------------
    '''
    if baseline:
        utils.mkdirs(os.path.join(baseline_dir, "SS"))
        ss_dir = os.path.join(baseline_dir, "SS/ss_vars.pkl")
        pickle.dump(ss_outputs, open(ss_dir, "wb"))
    else:
        utils.mkdirs(os.path.join(output_dir, "SS"))
        ss_dir = os.path.join(output_dir, "SS/ss_vars.pkl")
        pickle.dump(ss_outputs, open(ss_dir, "wb"))

